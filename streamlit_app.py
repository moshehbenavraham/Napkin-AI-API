import streamlit as st
import asyncio
import requests
import re
import subprocess
import os
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from src.core.generator import VisualGenerator
from src.utils.constants import STYLES
from src.utils.config import Settings

st.set_page_config(
    page_title="Napkin AI Visual Generator", page_icon="🎨", layout="wide"
)

st.title("🎨 Napkin AI Visual Generator")
st.markdown("Transform your text into beautiful visuals using AI")

# Constants
PNG_DEFAULT_WIDTH = 1920
PNG_DEFAULT_HEIGHT = 1080
MAX_TOTAL_PIXELS = 16777216  # 16 MP safety cap
MIN_CONTENT_LENGTH = 3  # basic sanity guard to avoid accidental empty prompts


def sanitize_filename(name: str) -> str:
    """Return a filesystem-friendly lowercase filename."""
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", name).strip("_").lower()


@st.cache_data(show_spinner=False)
def fetch_bytes(url: str, timeout: int = 30, api_token: Optional[str] = None) -> bytes:
    """
    Download bytes from a URL with optional Napkin API auth header.
    Cached by Streamlit to avoid redundant network calls across reruns.
    """
    headers: Dict[str, str] = {}
    if api_token and "api.napkin.ai" in url:
        headers["Authorization"] = f"Bearer {api_token}"
    resp = requests.get(url, timeout=timeout, headers=headers)
    resp.raise_for_status()
    return resp.content


def _render_svg(svg_bytes: bytes, *, height: Optional[int] = None, width: Optional[int] = None) -> None:
    """
    Render SVG bytes using an HTML <img> data URI to preserve vector fidelity.
    """
    import streamlit.components.v1 as components

    b64 = base64.b64encode(svg_bytes).decode("utf-8")
    style_dim = ""
    if width and height:
        style_dim = f"style='width:100%; max-width:{width}px;'"
    html = f"<img {style_dim} src='data:image/svg+xml;base64,{b64}'/>"
    components.html(html, height=height or 400, scrolling=False)


def run_generation_in_worker(
    api_token: str,
    content: str,
    selected_style: str,
    format_type: str,
    width: Optional[int],
    height: Optional[int],
    variations: int,
    transparent_background: bool = False,
    inverted_color: bool = False,
    language: Optional[str] = None,
    context_before: Optional[str] = None,
    context_after: Optional[str] = None,
    visual_id: Optional[str] = None,
    visual_query: Optional[str] = None,
):
    """
    Execute the async VisualGenerator.generate in a dedicated thread with its own event loop
    to avoid interfering with Streamlit's runtime.
    """

    def _runner():
        async def _gen():
            settings = Settings(napkin_api_token=api_token)
            async with VisualGenerator(settings) as generator:
                # generate returns a tuple of (StatusResponse, List[Path])
                status_response, _ = await generator.generate(
                    content=content,
                    style=selected_style,
                    format=format_type,
                    width=width,
                    height=height,
                    variations=variations,
                    save_files=False,  # Don't save to disk, just get URLs
                    transparent_background=transparent_background,
                    inverted_color=inverted_color,
                    language=language,
                    context_before=context_before,
                    context_after=context_after,
                    visual_id=visual_id,
                    visual_query=visual_query,
                )

                # Download the actual file content if we have API endpoints
                downloaded_files = []
                if hasattr(status_response, "files") and status_response.files:
                    for file_info in status_response.files:
                        if isinstance(file_info, dict):
                            # If we have an API endpoint URL, download it
                            if (
                                "url" in file_info
                                and "/v1/visual/" in file_info["url"]
                                and "/file/" in file_info["url"]
                            ):
                                # Parse the URL to get request_id and file_id
                                match = re.search(
                                    r"/v1/visual/([^/]+)/file/([^/]+)", file_info["url"]
                                )
                                if match:
                                    request_id, file_id = match.groups()
                                    # Remove any suffix like _c from file_id
                                    file_id = (
                                        file_id.split("_")[0]
                                        if "_" in file_id
                                        else file_id
                                    )
                                    try:
                                        # Download using the client
                                        content_bytes = (
                                            await generator.client.download_file(
                                                request_id, file_id
                                            )
                                        )
                                        # Store the content directly
                                        downloaded_files.append(
                                            {
                                                "content": content_bytes,
                                                "format": file_info.get(
                                                    "format", format_type
                                                ),
                                            }
                                        )
                                    except Exception:
                                        # If download fails, keep the original URL
                                        downloaded_files.append(file_info)
                            else:
                                # It's a direct URL, keep it as is
                                downloaded_files.append(file_info)
                        else:
                            # Not a dict, keep as is
                            downloaded_files.append(file_info)

                # Return a tuple with status_response and downloaded_files
                return (status_response, downloaded_files)

        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(_gen())
        finally:
            loop.close()

    with ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(_runner)
        return future.result()


with st.sidebar:
    st.header("⚙️ Settings")

    env_token = os.getenv("NAPKIN_API_TOKEN")
    api_token = env_token or st.text_input(
        "API Token",
        type="password",
        help="Enter your Napkin AI API token. You can also set it as NAPKIN_API_TOKEN environment variable.",
    )

    if env_token:
        st.info("Using API token from environment")

    if not api_token:
        st.error("⚠️ Please enter your API token to continue")

    st.divider()

    st.subheader("🎨 Style Selection")

    # Guard for empty STYLES
    if not STYLES:
        st.error("No styles available. Check your configuration.")
        st.stop()

    categories = sorted({s.category.value for s in STYLES.values()})
    if not categories:
        st.error("No style categories available. Check your configuration.")
        st.stop()

    style_category = st.selectbox(
        "Category",
        options=categories,
        help="Choose a style category to filter available styles",
    )

    filtered_styles = {
        k: v for k, v in STYLES.items() if v.category.value == style_category
    }
    if not filtered_styles:
        st.warning("No styles in this category.")
        st.stop()

    selected_style = st.selectbox(
        "Visual Style",
        options=list(filtered_styles.keys()),
        format_func=lambda x: f"{filtered_styles[x].name} - {filtered_styles[x].description}",
    )

    st.divider()

    st.subheader("📐 Format Options")

    format_type = st.radio(
        "Output Format",
        ["svg", "png"],
        help="SVG for scalable graphics, PNG for raster images",
    )

    col_w, col_h = st.columns(2)
    if format_type == "png":
        with col_w:
            width = st.number_input(
                "Width",
                min_value=100,
                max_value=4096,
                value=PNG_DEFAULT_WIDTH,
                step=100,
            )
        with col_h:
            height = st.number_input(
                "Height",
                min_value=100,
                max_value=4096,
                value=PNG_DEFAULT_HEIGHT,
                step=100,
            )

        # Pixel cap and hint
        total_px = int(width) * int(height)
        st.caption(f"Resolution: {width}×{height} (~{total_px/1_000_000:.1f} MP)")
        if total_px > MAX_TOTAL_PIXELS:
            st.warning(
                f"Resolution exceeds {MAX_TOTAL_PIXELS:,} pixels. Consider reducing size."
            )
            # Hard guard to prevent OOM or server overload
            st.stop()
    else:
        width = height = None

    variations = st.slider(
        "Number of Variations",
        min_value=1,
        max_value=4,
        value=1,
        help="Generate multiple variations of the same content",
    )

    st.divider()
    
    st.subheader("🎯 Advanced Options")
    
    # Transparency and color options
    col_trans, col_invert = st.columns(2)
    with col_trans:
        transparent_bg = st.checkbox(
            "Transparent Background",
            value=False,
            help="Use transparent background (works best with PNG)"
        )
    with col_invert:
        inverted_colors = st.checkbox(
            "Invert Colors",
            value=False,
            help="Invert the color scheme"
        )
    
    # Language selection
    languages = {
        "English": "en",
        "English (US)": "en-US", 
        "English (UK)": "en-GB",
        "Spanish": "es",
        "Spanish (Spain)": "es-ES",
        "Spanish (Mexico)": "es-MX",
        "French": "fr",
        "French (France)": "fr-FR",
        "German": "de",
        "German (Germany)": "de-DE",
        "Italian": "it",
        "Italian (Italy)": "it-IT",
        "Portuguese": "pt",
        "Portuguese (Brazil)": "pt-BR",
        "Dutch": "nl",
        "Dutch (Netherlands)": "nl-NL",
        "Russian": "ru",
        "Russian (Russia)": "ru-RU",
        "Chinese (Simplified)": "zh-CN",
        "Chinese (Traditional)": "zh-TW",
        "Japanese": "ja",
        "Japanese (Japan)": "ja-JP",
        "Korean": "ko",
        "Korean (Korea)": "ko-KR",
        "Arabic": "ar",
        "Hindi": "hi",
        "Turkish": "tr",
        "Turkish (Turkey)": "tr-TR",
        "Polish": "pl",
        "Polish (Poland)": "pl-PL",
        "Swedish": "sv",
        "Swedish (Sweden)": "sv-SE",
        "Danish": "da",
        "Danish (Denmark)": "da-DK",
        "Norwegian": "no",
        "Norwegian (Norway)": "no-NO",
        "Finnish": "fi",
        "Finnish (Finland)": "fi-FI"
    }
    
    selected_language = st.selectbox(
        "Language",
        options=list(languages.keys()),
        index=0,
        help="Select the language for your visual content (BCP 47 language tags)"
    )
    language_code = languages[selected_language]
    
    st.divider()
    
    st.subheader("🔄 Regeneration Options")
    st.caption("Optional: Regenerate existing visuals or search for specific visual types")
    
    with st.expander("Visual Regeneration Settings", expanded=False):
        regen_mode = st.radio(
            "Mode",
            ["New Visual", "Regenerate Existing", "Search Visual Type"],
            help="Choose how to generate your visual"
        )
        
        visual_id = None
        visual_query = None
        
        if regen_mode == "Regenerate Existing":
            visual_id = st.text_input(
                "Visual ID",
                placeholder="e.g., 5UCQJLAV5S6NXEWS2PBJF54UYPW5NZ4G",
                help="Enter the ID of an existing visual to regenerate with new content"
            )
            if visual_id and variations > 1:
                st.warning("⚠️ When regenerating, only 1 variation is allowed")
                variations = 1
                
        elif regen_mode == "Search Visual Type":
            visual_types = [
                "mindmap",
                "flowchart",
                "timeline",
                "diagram",
                "infographic",
                "chart",
                "graph",
                "process",
                "hierarchy",
                "network",
                "venn",
                "matrix",
                "cycle",
                "pyramid",
                "funnel"
            ]
            visual_query = st.selectbox(
                "Visual Type",
                options=visual_types,
                help="Search for a specific type of visual"
            )

    st.divider()

    with st.expander("ℹ️ About Styles", expanded=False):
        if selected_style in filtered_styles:
            selected_style_info = filtered_styles[selected_style]
            st.write(f"**{selected_style_info.name}**")
            st.write(f"*{selected_style_info.description}*")
            st.write(f"Category: {selected_style_info.category.value}")
        else:
            st.write("Selected style not found in current category.")

# Context fields
with st.expander("📋 Context Options (Optional)", expanded=False):
    st.caption("Add context to help generate more meaningful visuals")
    context_before = st.text_input(
        "Context Before",
        placeholder="e.g., 'Introduction to' or 'Welcome to'",
        help="Text context that appears before the main content"
    )
    context_after = st.text_input(
        "Context After",
        placeholder="e.g., 'for beginners' or 'explained simply'",
        help="Text context that appears after the main content"
    )

content = st.text_area(
    "📝 Enter your content to visualize:",
    height=200,
    placeholder="Describe what you want to visualize... For example:\n\n- A workflow diagram showing user authentication process\n- The solar system with all planets and their orbits\n- A mind map about machine learning concepts\n- An infographic about climate change statistics",
    help="Be descriptive! The more detail you provide, the better the visual will be.",
)
trimmed_content = content.strip()

col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    ready = bool(api_token) and bool(trimmed_content)
    generate_button = st.button(
        "🚀 Generate Visual",
        type="primary",
        use_container_width=True,
        disabled=not ready,
    )
with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

if clear_button:
    st.rerun()

if generate_button:
    if not trimmed_content:
        st.error("❌ Please enter some content to visualize")
    elif len(trimmed_content) < MIN_CONTENT_LENGTH:
        st.error("❌ Content is too short. Please provide more details.")
    elif not api_token:
        st.error("❌ API token is required. Please enter it in the sidebar.")
    else:
        with st.spinner(
            f"🎨 Generating {variations} visual(s) in {selected_style} style..."
        ):

            async def generate():
                settings = Settings(napkin_api_token=api_token)
                async with VisualGenerator(settings) as generator:
                    return await generator.generate(
                        content=content,
                        style=selected_style,
                        format=format_type,
                        width=width,
                        height=height,
                        variations=variations,
                    )

            try:
                # Run async generation in a dedicated worker thread/event loop
                result = run_generation_in_worker(
                    api_token=api_token,
                    content=trimmed_content,
                    selected_style=selected_style,
                    format_type=format_type,
                    width=width,
                    height=height,
                    variations=variations,
                    transparent_background=transparent_bg,
                    inverted_color=inverted_colors,
                    language=language_code,
                    context_before=context_before if 'context_before' in locals() and context_before else None,
                    context_after=context_after if 'context_after' in locals() and context_after else None,
                    visual_id=visual_id if 'visual_id' in locals() and visual_id else None,
                    visual_query=visual_query if 'visual_query' in locals() and visual_query else None,
                )

                # Defensive: result could be None or a tuple
                if result is None:
                    st.error("No response from generator. Please try again.")
                    st.stop()

                # Check if we have downloaded files
                files_to_display: List[Any] = []
                
                # Handle tuple response (status_response, downloaded_files)
                if isinstance(result, tuple) and len(result) == 2:
                    status_response, downloaded_files = result
                    if downloaded_files:
                        files_to_display = downloaded_files
                    elif hasattr(status_response, "files") and getattr(status_response, "files"):
                        files_to_display = status_response.files
                    # Update result to be just the status_response for later usage
                    result = status_response
                elif hasattr(result, "files") and getattr(result, "files"):
                    # Fallback to URL-based files
                    files_to_display = result.files

                if not files_to_display:
                    st.error("No files were generated. Please try again.")
                    st.stop()

                st.success(
                    f"✅ Successfully generated {len(files_to_display)} visual(s)!"
                )

                st.divider()
                st.subheader("🖼️ Generated Visuals")

                # Choose a balanced grid up to 3 columns for multiple variations
                grid_cols = 1 if variations == 1 else min(variations, 3)
                cols = st.columns(grid_cols)

                for idx, file_data in enumerate(files_to_display):
                    target_col = cols[0] if grid_cols == 1 else cols[idx % grid_cols]
                    with target_col:
                        content_bytes = None

                        if isinstance(file_data, dict):
                            if "content" in file_data:
                                # Pre-downloaded content
                                content_bytes = file_data["content"]
                            elif "url" in file_data:
                                # Try to fetch from URL
                                try:
                                    content_bytes = fetch_bytes(
                                        file_data["url"],
                                        timeout=30,
                                        api_token=api_token,
                                    )
                                except requests.RequestException as re:
                                    st.warning(f"Failed to fetch visual v{idx+1}: {re}")
                                    continue
                        elif isinstance(file_data, str):
                            # Direct URL
                            try:
                                content_bytes = fetch_bytes(
                                    file_data, timeout=30, api_token=api_token
                                )
                            except requests.RequestException as re:
                                st.warning(f"Failed to fetch visual v{idx+1}: {re}")
                                continue

                        if not content_bytes:
                            st.warning(f"No content available for visual v{idx+1}")
                            continue

                        mime = "image/png" if format_type == "png" else "image/svg+xml"

                        # Display according to format
                        if format_type == "png":
                            st.image(content_bytes, use_container_width=True, caption=None)
                        else:
                            # Render SVG preserving vector quality
                            _render_svg(content_bytes)

                        file_name = (
                            f"napkin_{sanitize_filename(selected_style)}"
                            + (f"_v{idx+1}" if variations > 1 else f"_{idx+1}")
                            + f".{format_type}"
                        )

                        st.download_button(
                            label=f"⬇️ Download{' v'+str(idx+1) if variations>1 else ''}",
                            data=content_bytes,
                            file_name=file_name,
                            mime=mime,
                            use_container_width=True,
                        )

                with st.expander("📊 Generation Details"):
                    details = {
                        "request_id": getattr(result, "request_id", None),
                        "style": selected_style,
                        "format": format_type,
                        "variations": variations,
                        "dimensions": f"{width}x{height}"
                        if width
                        else "SVG (scalable)",
                        "files_generated": len(files_to_display),
                        "language": language_code if 'language_code' in locals() else None,
                        "transparent_background": transparent_bg if 'transparent_bg' in locals() else False,
                        "inverted_colors": inverted_colors if 'inverted_colors' in locals() else False,
                    }
                    if 'context_before' in locals() and context_before:
                        details["context_before"] = context_before
                    if 'context_after' in locals() and context_after:
                        details["context_after"] = context_after
                    if 'visual_id' in locals() and visual_id:
                        details["visual_id"] = visual_id
                    if 'visual_query' in locals() and visual_query:
                        details["visual_query"] = visual_query
                    st.json(details)

            except Exception as e:
                st.error(f"❌ Generation failed: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.code(repr(e))

st.divider()

with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📚 Resources")
        st.markdown("- [Napkin AI](https://napkin.ai)")
        st.markdown("- [API Documentation](https://docs.napkin.ai)")
        st.markdown("- [Style Gallery](https://napkin.ai/styles)")
    with col2:
        st.markdown("### 🎨 Available Styles")
        st.markdown(
            f"**{len(STYLES)}** unique visual styles across **{len(categories)}** categories"
        )
    with col3:
        st.markdown("### 💡 Tips")
        st.markdown("- Be descriptive in your content")
        st.markdown("- Try different styles for the same content")
        st.markdown("- Generate multiple variations for options")

st.markdown("---")

# Version info in footer


@st.cache_resource(show_spinner=False)
def get_git_info() -> str:
    """Return a short version string including branch@commit if available."""
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True
        ).strip()
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"], text=True
        ).strip()
        return f"v0.2.2 | {branch}@{commit}"
    except Exception:
        return "v0.2.2"


version_info = get_git_info()
deploy_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

st.markdown(
    f"<div style='text-align: center; color: #888;'>"
    f"Powered by <a href='https://napkin.ai'>Napkin AI</a> | "
    f"Built with <a href='https://streamlit.io'>Streamlit</a><br>"
    f"<small>{version_info} | Last updated: {deploy_time}</small>"
    f"</div>",
    unsafe_allow_html=True,
)
