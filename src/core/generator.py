"""
Core visual generation logic for Napkin AI API.

Provides high-level interface for generating visuals through the API,
handling the complete workflow from request to downloaded files.
"""

import asyncio
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple

from ..api.client import NapkinAPIClient, ProcessingError
from ..api.models import VisualRequest, VisualResponse, StatusResponse, GeneratedFile
from ..utils.config import Settings, get_settings
from ..utils.constants import STYLES, get_style_by_name


logger = logging.getLogger(__name__)


class VisualGenerator:
    """High-level interface for visual generation."""
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize visual generator.
        
        Args:
            settings: Configuration settings. If None, loads from environment.
        """
        self.settings = settings or get_settings()
        self.client: Optional[NapkinAPIClient] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.client = NapkinAPIClient(self.settings)
        await self.client.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)
    
    def _prepare_request(
        self,
        content: str,
        style: Optional[str] = None,
        format: Optional[str] = None,
        language: Optional[str] = None,
        variations: Optional[int] = None,
        context_before: Optional[str] = None,
        context_after: Optional[str] = None,
        transparent: bool = False,
        inverted: bool = False,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> VisualRequest:
        """
        Prepare visual request with defaults.
        
        Args:
            content: Text content to visualize.
            style: Style name or ID.
            format: Output format (svg/png).
            language: Language code.
            variations: Number of variations (1-4).
            context_before: Context before content.
            context_after: Context after content.
            transparent: Enable transparent background.
            inverted: Invert colors.
            width: Width in pixels (PNG only).
            height: Height in pixels (PNG only).
        
        Returns:
            Prepared VisualRequest.
        """
        # Apply defaults
        format = format or self.settings.default_format
        language = language or self.settings.default_language
        variations = variations or self.settings.default_variations
        
        # Handle style - could be name or ID
        style_id = None
        if style:
            # Check if it's a known style name
            try:
                style_obj = get_style_by_name(style)
                style_id = style_obj.id
            except ValueError:
                # Assume it's a custom style ID
                style_id = style
        else:
            # Use default style
            try:
                style_obj = get_style_by_name(self.settings.default_style)
                style_id = style_obj.id
            except ValueError:
                style_id = self.settings.default_style
        
        # Create request
        return VisualRequest(
            content=content,
            format=format,
            style_id=style_id,
            language=language,
            number_of_visuals=variations,
            context_before=context_before,
            context_after=context_after,
            transparent_background=transparent,
            inverted_color=inverted,
            width=width,
            height=height,
        )
    
    def _generate_filename(
        self,
        request_id: str,
        file_id: str,
        format: str,
        index: int = 0,
    ) -> str:
        """
        Generate filename for saved visual.
        
        Args:
            request_id: Request ID.
            file_id: File ID.
            format: File format.
            index: File index for multiple variations.
        
        Returns:
            Generated filename.
        """
        # Use timezone-aware UTC and consistent filename pattern
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        if index > 0:
            return f"napkin_{timestamp}_{request_id[:8]}_v{index + 1}.{format}"
        return f"napkin_{timestamp}_{request_id[:8]}.{format}"
    
    async def generate(
        self,
        content: str,
        output_dir: Optional[Path] = None,
        style: Optional[str] = None,
        format: Optional[str] = None,
        language: Optional[str] = None,
        variations: Optional[int] = None,
        context_before: Optional[str] = None,
        context_after: Optional[str] = None,
        transparent: bool = False,
        inverted: bool = False,
        width: Optional[int] = None,
        height: Optional[int] = None,
        save_files: bool = True,
    ) -> Tuple[StatusResponse, List[Path]]:
        """
        Generate visuals from text content.
        
        Args:
            content: Text content to visualize.
            output_dir: Directory to save files (uses config default if None).
            style: Style name or ID.
            format: Output format (svg/png).
            language: Language code.
            variations: Number of variations (1-4).
            context_before: Context before content.
            context_after: Context after content.
            transparent: Enable transparent background.
            inverted: Invert colors.
            width: Width in pixels (PNG only).
            height: Height in pixels (PNG only).
            save_files: Whether to save files to disk.
        
        Returns:
            Tuple of (final status, list of saved file paths).
        
        Raises:
            ProcessingError: If generation fails.
        """
        if not self.client:
            raise RuntimeError("Generator must be used as async context manager")
        
        # Prepare request
        request = self._prepare_request(
            content=content,
            style=style,
            format=format,
            language=language,
            variations=variations,
            context_before=context_before,
            context_after=context_after,
            transparent=transparent,
            inverted=inverted,
            width=width,
            height=height,
        )
        
        # Log generation start
        logger.info(f"Generating {request.number_of_visuals} visual(s) in {request.format} format")
        
        # Create visual request
        response = await self.client.create_visual(request)
        request_id = response.request_id
        
        logger.info(f"Request created: {request_id}")
        
        # Wait for completion
        final_status = await self.client.wait_for_completion(request_id)
        
        if final_status.status.value != "completed":
            raise ProcessingError(f"Generation failed: {final_status.error or 'Unknown error'}")
        
        logger.info(f"Generation completed: {final_status.files_ready} file(s) ready")
        
        # Download files if requested
        saved_paths = []
        if save_files and final_status.files_ready > 0:
            output_dir = output_dir or self.settings.storage_path
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Get files from status response (normalized by client.get_status)
            files = getattr(final_status, "files", []) or []

            def _infer_ext(fmt: Optional[str], url: Optional[str]) -> str:
                if fmt in {"svg", "png"}:
                    return fmt
                if url:
                    if ".svg" in url.lower() or "image/svg" in url.lower():
                        return "svg"
                    if ".png" in url.lower():
                        return "png"
                # Fallback to requested format
                return request.format.value if hasattr(request, "format") else "svg"

            if files:
                for i, file_info in enumerate(files):
                    # file_info may be dict with {id, url?, format?, filename?} or {"url": "..."} from urls mapping
                    file_id = file_info.get("id", f"file_{i + 1}")
                    file_url = file_info.get("url")
                    file_fmt = _infer_ext(file_info.get("format"), file_url)

                    # Prefer provided filename if present; else generate
                    filename = file_info.get("filename") or self._generate_filename(
                        request_id, file_id, file_fmt, i
                    )
                    file_path = output_dir / filename

                    try:
                        if file_url:
                            # Use client direct URL downloader for consistent headers/handling
                            content = await self.client.download_file_by_url(file_url)
                            file_path.write_bytes(content)
                            saved_paths.append(file_path)
                            logger.info("Saved: %s", file_path)
                        else:
                            # Fall back to file ID endpoint
                            await self.client.download_file(
                                request_id,
                                file_id,
                                file_path,
                            )
                            saved_paths.append(file_path)
                            logger.info("Saved: %s", file_path)
                    except Exception as e:
                        logger.error("Failed to download file %s: %s", file_id, e)
            else:
                # Fallback path when API doesn't return file metadata; try sequential IDs
                for i in range(final_status.files_ready):
                    file_id = f"file_{i + 1}"
                    filename = self._generate_filename(
                        request_id, file_id, request.format.value, i
                    )
                    file_path = output_dir / filename
                    try:
                        await self.client.download_file(
                            request_id,
                            file_id,
                            file_path,
                        )
                        saved_paths.append(file_path)
                        logger.info("Saved: %s", file_path)
                    except Exception as e:
                        logger.error("Failed to download file %s: %s", file_id, e)
        
        return final_status, saved_paths
    
    async def generate_batch(
        self,
        contents: List[str],
        output_dir: Optional[Path] = None,
        style: Optional[str] = None,
        format: Optional[str] = None,
        concurrent_limit: Optional[int] = None,
        **kwargs,
    ) -> List[Tuple[str, StatusResponse, List[Path]]]:
        """
        Generate visuals for multiple contents in batch.
        
        Args:
            contents: List of text contents.
            output_dir: Directory to save files.
            style: Style name or ID.
            format: Output format.
            concurrent_limit: Max concurrent requests.
            **kwargs: Additional generation parameters.
        
        Returns:
            List of tuples (content, status, file_paths) for each generation.
        """
        concurrent_limit = concurrent_limit or self.settings.batch_concurrent_limit
        
        # Create semaphore for rate limiting
        semaphore = asyncio.Semaphore(concurrent_limit)
        
        async def generate_one(content: str, index: int):
            """Generate visual for one content item."""
            async with semaphore:
                try:
                    # Create subdirectory for batch item
                    item_dir = None
                    if output_dir:
                        item_dir = output_dir / f"batch_{index + 1:03d}"
                    
                    status, paths = await self.generate(
                        content=content,
                        output_dir=item_dir,
                        style=style,
                        format=format,
                        **kwargs,
                    )
                    return content, status, paths
                except Exception as e:
                    logger.error(f"Failed to generate visual for item {index + 1}: {e}")
                    return content, None, []
        
        # Generate all visuals concurrently
        tasks = [
            generate_one(content, i)
            for i, content in enumerate(contents)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Log summary
        successful = sum(1 for _, status, _ in results if status)
        logger.info(f"Batch generation completed: {successful}/{len(contents)} successful")
        
        return results


async def generate_visual(
    content: str,
    output_dir: Optional[Path] = None,
    style: Optional[str] = None,
    format: Optional[str] = None,
    **kwargs,
) -> Tuple[StatusResponse, List[Path]]:
    """
    Convenience function to generate a visual.
    
    Args:
        content: Text content to visualize.
        output_dir: Directory to save files.
        style: Style name or ID.
        format: Output format.
        **kwargs: Additional generation parameters.
    
    Returns:
        Tuple of (status, file_paths).
    """
    async with VisualGenerator() as generator:
        return await generator.generate(
            content=content,
            output_dir=output_dir,
            style=style,
            format=format,
            **kwargs,
        )