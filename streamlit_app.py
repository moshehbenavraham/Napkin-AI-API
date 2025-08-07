import streamlit as st
import asyncio
import requests
import re
from src.core.generator import VisualGenerator
from src.utils.constants import STYLES
from src.utils.config import Settings
import os
from concurrent.futures import ThreadPoolExecutor

st.set_page_config(
    page_title="Napkin AI Visual Generator",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Napkin AI Visual Generator")
st.markdown("Transform your text into beautiful visuals using AI")

# Constants
PNG_DEFAULT_WIDTH = 1920
PNG_DEFAULT_HEIGHT = 1080
MAX_TOTAL_PIXELS = 16777216  # 16 MP safety cap

def sanitize_filename(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", name).strip("_").lower()

def fetch_bytes(url: str, timeout: int = 30) -> bytes:
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.content

def run_generation_in_worker(api_token: str, content: str, selected_style: str, format_type: str, width, height, variations: int):
    """
    Execute the async VisualGenerator.generate in a dedicated thread with its own event loop
    to avoid interfering with Streamlit's runtime.
    """
    def _runner():
        async def _gen():
            settings = Settings(napkin_api_token=api_token)
            async with VisualGenerator(settings) as generator:
                return await generator.generate(
                    content=content,
                    style=selected_style,
                    format=format_type,
                    width=width,
                    height=height,
                    variations=variations
                )
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
        help="Enter your Napkin AI API token. You can also set it as NAPKIN_API_TOKEN environment variable."
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
        help="Choose a style category to filter available styles"
    )

    filtered_styles = {k: v for k, v in STYLES.items() if v.category.value == style_category}
    if not filtered_styles:
        st.warning("No styles in this category.")
        st.stop()

    selected_style = st.selectbox(
        "Visual Style",
        options=list(filtered_styles.keys()),
        format_func=lambda x: f"{filtered_styles[x].name} - {filtered_styles[x].description}"
    )

    st.divider()

    st.subheader("📐 Format Options")

    format_type = st.radio(
        "Output Format",
        ["svg", "png"],
        help="SVG for scalable graphics, PNG for raster images"
    )

    col_w, col_h = st.columns(2)
    if format_type == "png":
        with col_w:
            width = st.number_input("Width", min_value=100, max_value=4096, value=PNG_DEFAULT_WIDTH, step=100)
        with col_h:
            height = st.number_input("Height", min_value=100, max_value=4096, value=PNG_DEFAULT_HEIGHT, step=100)

        # Pixel cap and hint
        total_px = width * height
        st.caption(f"Resolution: {width}×{height} (~{total_px/1_000_000:.1f} MP)")
        if total_px > MAX_TOTAL_PIXELS:
            st.warning(f"Resolution exceeds {MAX_TOTAL_PIXELS:,} pixels. Consider reducing size.")
    else:
        width = height = None

    variations = st.slider(
        "Number of Variations",
        min_value=1,
        max_value=4,
        value=1,
        help="Generate multiple variations of the same content"
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

content = st.text_area(
    "📝 Enter your content to visualize:",
    height=200,
    placeholder="Describe what you want to visualize... For example:\n\n- A workflow diagram showing user authentication process\n- The solar system with all planets and their orbits\n- A mind map about machine learning concepts\n- An infographic about climate change statistics",
    help="Be descriptive! The more detail you provide, the better the visual will be."
)

col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    ready = bool(api_token) and bool(content.strip())
    generate_button = st.button("🚀 Generate Visual", type="primary", use_container_width=True, disabled=not ready)
with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

if clear_button:
    st.rerun()

if generate_button:
    if not content.strip():
        st.error("❌ Please enter some content to visualize")
    elif not api_token:
        st.error("❌ API token is required. Please enter it in the sidebar.")
    else:
        with st.spinner(f"🎨 Generating {variations} visual(s) in {selected_style} style..."):
            async def generate():
                settings = Settings(napkin_api_token=api_token)
                async with VisualGenerator(settings) as generator:
                    return await generator.generate(
                        content=content,
                        style=selected_style,
                        format=format_type,
                        width=width,
                        height=height,
                        variations=variations
                    )
            
            try:
                # Run async generation in a dedicated worker thread/event loop
                result = run_generation_in_worker(
                    api_token=api_token,
                    content=content,
                    selected_style=selected_style,
                    format_type=format_type,
                    width=width,
                    height=height,
                    variations=variations
                )

                st.success(f"✅ Successfully generated {len(result.files)} visual(s)!")

                st.divider()
                st.subheader("🖼️ Generated Visuals")

                # Choose a balanced grid up to 3 columns for multiple variations
                grid_cols = 1 if variations == 1 else min(variations, 3)
                cols = st.columns(grid_cols)

                for idx, file_url in enumerate(result.files):
                    target_col = cols[0] if grid_cols == 1 else cols[idx % grid_cols]
                    with target_col:
                        try:
                            content_bytes = fetch_bytes(file_url, timeout=30)
                        except requests.RequestException as re:
                            st.warning(f"Failed to fetch visual v{idx+1}: {re}")
                            continue

                        mime = "image/png" if format_type == "png" else "image/svg+xml"
                        st.image(content_bytes, use_container_width=True, caption=None)

                        file_name = f"napkin_{sanitize_filename(selected_style)}" + \
                                    (f"_v{idx+1}" if variations > 1 else f"_{idx+1}") + \
                                    f".{format_type}"

                        st.download_button(
                            label=f"⬇️ Download{' v'+str(idx+1) if variations>1 else ''}",
                            data=content_bytes,
                            file_name=file_name,
                            mime=mime,
                            use_container_width=True
                        )

                with st.expander("📊 Generation Details"):
                    st.json({
                        "request_id": getattr(result, "request_id", None),
                        "style": selected_style,
                        "format": format_type,
                        "variations": variations,
                        "dimensions": f"{width}x{height}" if width else "SVG (scalable)",
                        "files_generated": len(result.files)
                    })

            except Exception as e:
                st.error(f"❌ Generation failed: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.code(str(e))

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
        st.markdown(f"**{len(STYLES)}** unique visual styles across **{len(categories)}** categories")
    with col3:
        st.markdown("### 💡 Tips")
        st.markdown("- Be descriptive in your content")
        st.markdown("- Try different styles for the same content")
        st.markdown("- Generate multiple variations for options")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>Powered by <a href='https://napkin.ai'>Napkin AI</a> | "
    "Built with <a href='https://streamlit.io'>Streamlit</a></div>",
    unsafe_allow_html=True
)