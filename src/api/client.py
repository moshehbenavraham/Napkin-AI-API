"""  
Napkin AI API client with async support and retry logic.

Provides a robust HTTP client for interacting with the Napkin API,
including authentication, rate limiting, and exponential backoff.
"""

import asyncio
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Union

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log,
)

from ..utils.config import Settings, get_settings
from ..utils.constants import API_ENDPOINTS, HTTP_STATUS
from .models import (
    ErrorResponse,
    GeneratedFile,
    RateLimitInfo,
    RequestStatus,
    StatusResponse,
    VisualRequest,
    VisualResponse,
)


logger = logging.getLogger(__name__)


class NapkinAPIError(Exception):
    """Base exception for Napkin API errors."""
    
    def __init__(self, message: str, code: Optional[str] = None, details: Optional[dict] = None):
        super().__init__(message)
        self.code = code
        self.details = details


class AuthenticationError(NapkinAPIError):
    """Authentication failed."""
    pass


class RateLimitError(NapkinAPIError):
    """Rate limit exceeded."""
    
    def __init__(self, message: str, retry_after: int):
        super().__init__(message)
        self.retry_after = retry_after


class RequestError(NapkinAPIError):
    """Request validation error."""
    pass


class ProcessingError(NapkinAPIError):
    """Visual processing error."""
    pass


class NapkinAPIClient:
    """Async client for Napkin AI API."""
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize API client.
        
        Args:
            settings: Configuration settings. If None, loads from environment.
        """
        self.settings = settings or get_settings()
        self.base_url = f"{self.settings.api_base_url}/{self.settings.api_version}"
        self.headers = self.settings.get_headers()
        
        # HTTP client with timeout
        # Allow optional client injection and granular timeouts
        self._owns_client = True
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(
                connect=self.settings.timeout_seconds,
                read=self.settings.timeout_seconds,
                write=self.settings.timeout_seconds,
                pool=self.settings.timeout_seconds,
            ),
            headers=self.headers,
        )
        
        # Rate limit tracking
        self.rate_limit_info: Optional[RateLimitInfo] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def close(self):
        """Close HTTP client."""
        # Close only if owned by this instance
        if getattr(self, "_owns_client", True):
            await self.client.aclose()
    
    def _extract_rate_limit_info(self, response: httpx.Response) -> Optional[RateLimitInfo]:
        """Extract rate limit information from response headers."""
        try:
            headers = response.headers

            if "X-RateLimit-Limit" in headers or "Retry-After" in headers:
                # Parse limit/remaining defensively
                try:
                    limit = int(headers.get("X-RateLimit-Limit", "60"))
                except (ValueError, TypeError):
                    limit = 60
                try:
                    remaining = int(headers.get("X-RateLimit-Remaining", "0"))
                except (ValueError, TypeError):
                    remaining = 0

                # Parse reset timestamp robustly
                reset = None
                reset_hdr = headers.get("X-RateLimit-Reset")
                retry_after_val = headers.get("Retry-After")

                try:
                    if reset_hdr is not None:
                        reset = datetime.fromtimestamp(int(reset_hdr))
                except (ValueError, TypeError, OSError):
                    # If reset is invalid but Retry-After present, compute approximate reset
                    if retry_after_val is not None:
                        try:
                            ra = int(retry_after_val)
                            # Use timezone-aware UTC
                            reset = datetime.fromtimestamp(int(datetime.now(timezone.utc).timestamp()) + ra, tz=timezone.utc)
                        except (ValueError, TypeError):
                            reset = None

                # Parse retry-after seconds
                retry_after = None
                try:
                    if retry_after_val is not None:
                        retry_after = int(retry_after_val)
                except (ValueError, TypeError):
                    retry_after = None

                return RateLimitInfo(
                    limit=limit,
                    remaining=remaining,
                    reset=reset,
                    retry_after=retry_after,
                )
        except Exception as e:
            logger.warning(f"Failed to parse rate limit headers: {e}")
        return None
    
    def _handle_error_response(self, response: httpx.Response):
        """Handle API error responses."""
        try:
            error_data = response.json()
            error_msg = error_data.get("error", "Unknown error")
            error_code = error_data.get("code")
            details = error_data.get("details")
        except Exception:
            error_msg = response.text or f"HTTP {response.status_code} error"
            error_code = None
            details = None
        
        # Check for specific error types
        if response.status_code == HTTP_STATUS["unauthorized"]:
            raise AuthenticationError(error_msg, error_code, details)
        elif response.status_code == HTTP_STATUS["rate_limit"]:
            retry_after = int(response.headers.get("Retry-After", "60"))
            raise RateLimitError(error_msg, retry_after)
        elif response.status_code == HTTP_STATUS["bad_request"]:
            raise RequestError(error_msg, error_code, details)
        else:
            raise NapkinAPIError(error_msg, error_code, details)
    
    @retry(
        retry=retry_if_exception_type(httpx.HTTPError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ) -> httpx.Response:
        """Make HTTP request with retry logic."""
        url = f"{self.base_url}{endpoint}"
        
        logger.debug(f"{method} {url}")
        
        response = await self.client.request(method, url, **kwargs)
        
        # Update rate limit info
        self.rate_limit_info = self._extract_rate_limit_info(response)
        
        # Handle errors
        if response.status_code >= 400:
            self._handle_error_response(response)
        
        return response
    
    async def create_visual(
        self,
        request: VisualRequest,
    ) -> VisualResponse:
        """
        Create a new visual generation request.
        
        Args:
            request: Visual generation parameters.
        
        Returns:
            VisualResponse with request ID and initial status.
        
        Raises:
            NapkinAPIError: If request fails.
        """
        endpoint = API_ENDPOINTS["create_visual"]
        
        # Prepare request data
        request_data = request.model_dump(exclude_none=True)
        
        # Log request without leaking content
        try:
            content_len = len(getattr(request, "content", "") or "")
        except Exception:
            content_len = 0
        logger.info("Creating visual request (content_length=%d)", content_len)
        
        # Make API call
        response = await self._make_request(
            "POST",
            endpoint,
            json=request_data,
        )
        
        # Parse response
        response_data = response.json()
        logger.debug(f"Create visual response: {response_data}")
        
        # Create response model
        return VisualResponse(
            request_id=response_data.get("id") or response_data.get("request_id"),
            status=RequestStatus(response_data.get("status", "pending")),
            created_at=self._parse_iso8601(response_data["created_at"]) if "created_at" in response_data else datetime.now(timezone.utc),
            files=[],
        )
    
    def _parse_iso8601(self, s: str) -> datetime:
        """Parse ISO8601 timestamps, supporting trailing 'Z', returning timezone-aware UTC on fallback."""
        try:
            if s.endswith("Z"):
                return datetime.fromisoformat(s.replace("Z", "+00:00"))
            dt = datetime.fromisoformat(s)
            # Ensure timezone-aware; default to UTC if naive
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except Exception:
            return datetime.now(timezone.utc)
    
    async def get_status(
        self,
        request_id: str,
    ) -> StatusResponse:
        """
        Check status of a visual generation request.
        
        Args:
            request_id: The request ID to check.
        
        Returns:
            StatusResponse with current status and progress.
        
        Raises:
            NapkinAPIError: If request fails.
        """
        endpoint = API_ENDPOINTS["get_status"].format(request_id=request_id)
        
        # Make API call
        response = await self._make_request("GET", endpoint)

        # Parse response and emit DEBUG to inspect actual structure
        response_data = response.json()
        logger.debug("Status response for %s: %s", request_id, response_data)

        # The API may return:
        #   - generated_files: [{ id, url, format, filename?, size_bytes? }]
        #   - files:            same shape (legacy/alternate key)
        #   - urls:             [ "https://..." ] (legacy minimal)
        # Normalize while preserving raw structure in .files
        raw_generated = response_data.get("generated_files")
        raw_files = response_data.get("files")
        raw_urls = response_data.get("urls")

        # Prefer generated_files if present
        candidate = None
        if isinstance(raw_generated, list):
            candidate = raw_generated
        elif isinstance(raw_files, list):
            candidate = raw_files
        elif isinstance(raw_urls, list):
            candidate = [{"url": u} for u in raw_urls]

        if candidate is not None:
            files_ready = len(candidate)
            files_total = len(candidate)
        else:
            files_ready = int(response_data.get("files_ready", 0) or 0)
            files_total = int(response_data.get("files_total", 0) or 0)

        status_resp = StatusResponse(
            request_id=request_id,
            status=RequestStatus(response_data["status"]),
            progress=response_data.get("progress"),
            message=response_data.get("message"),
            files_ready=files_ready,
            files_total=files_total,
            error=response_data.get("error"),
        )

        # Preserve whichever structure we received for downstream logic
        if candidate is not None:
            status_resp.files = candidate  # type: ignore[assignment]

        return status_resp
    
    async def download_file(
        self,
        request_id: str,
        file_id: str,
        save_path: Optional[Path] = None,
    ) -> Union[bytes, Path]:
        """
        Download a generated file by request/file ID.
        Streams to disk if save_path is provided to avoid large memory usage.
        """
        endpoint = API_ENDPOINTS["get_file"].format(
            request_id=request_id,
            file_id=file_id,
        )
        url = f"{self.base_url}{endpoint}"
        return await self._stream_or_bytes(url, save_path)

    async def save_file_by_url(
        self,
        url: str,
        output_dir: Union[str, Path],
        inferred_name: Optional[str] = None,
        request_id: Optional[str] = None,
        file_id: Optional[str] = None,
    ) -> Path:
        """
        Stream a file from a signed/authorized URL to disk with filename inference.
        - Parses Content-Disposition for filename (RFC 6266/5987)
        - Falls back to provided inferred_name, then API metadata (request_id/file_id), then URL path
        - Respects NAPKIN_DOWNLOAD_CHUNK_SIZE and NAPKIN_DOWNLOAD_OVERWRITE
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Make streaming GET to obtain headers
        async with self.client.stream("GET", url, headers=self.headers) as r:
            if r.status_code >= 400:
                body = await r.aread()
                resp = httpx.Response(status_code=r.status_code, headers=r.headers, content=body, request=r.request)
                self._handle_error_response(resp)

            # Determine filename
            cd = r.headers.get("Content-Disposition", "") or r.headers.get("content-disposition", "")
            filename = self._infer_filename_from_content_disposition(cd)
            if not filename:
                filename = inferred_name

            if not filename:
                # Try to infer from request/file/meta
                ext = self._infer_extension_from_content_type(r.headers.get("Content-Type"))
                base = None
                if request_id and file_id:
                    base = f"{request_id}_{file_id}"
                elif file_id:
                    base = file_id
                # Fallback to URL path segment
                if not base:
                    try:
                        base = Path(httpx.URL(url).path).name or "download"
                    except Exception:
                        base = "download"
                filename = f"{base}.{ext}" if ext and not base.endswith(f".{ext}") else (base if base else "download")

            # Prepare final path and overwrite policy
            dest = output_dir / filename
            overwrite = self._get_bool_env("NAPKIN_DOWNLOAD_OVERWRITE", default=False)
            if dest.exists() and not overwrite:
                # Avoid clobber; add numeric suffix
                dest = self._dedupe_path(dest)

            # Chunked write
            chunk_size = self._get_int_env("NAPKIN_DOWNLOAD_CHUNK_SIZE", default=65536)
            with dest.open("wb") as f:
                async for chunk in r.aiter_bytes(chunk_size=chunk_size):
                    f.write(chunk)

        logger.info("Saved file to %s", dest)
        return dest

    async def _stream_or_bytes(self, url: str, save_path: Optional[Path]) -> Union[bytes, Path]:
        """
        Helper to stream to disk if save_path is provided, otherwise return bytes.
        """
        if save_path:
            save_path = Path(save_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            async with self.client.stream("GET", url, headers=self.headers) as r:
                if r.status_code >= 400:
                    body = await r.aread()
                    resp = httpx.Response(status_code=r.status_code, headers=r.headers, content=body, request=r.request)
                    self._handle_error_response(resp)
                with save_path.open("wb") as f:
                    async for chunk in r.aiter_bytes():
                        f.write(chunk)
            logger.info("Saved file to %s", save_path)
            return save_path
        # Return bytes
        resp = await self.client.get(url, headers=self.headers)
        if resp.status_code >= 400:
            self._handle_error_response(resp)
        return resp.content

    def _infer_extension_from_content_type(self, content_type: Optional[str]) -> Optional[str]:
        """
        Map MIME type to file extension; default to svg/png only.
        """
        if not content_type:
            return None
        ct = content_type.split(";")[0].strip().lower()
        if ct == "image/svg+xml":
            return "svg"
        if ct == "image/png":
            return "png"
        return None

    def _infer_filename_from_content_disposition(self, cd: Optional[str]) -> Optional[str]:
        """
        Parse Content-Disposition for filename* (RFC 5987) or filename.
        """
        if not cd:
            return None
        try:
            # naive parse; sufficient for common cases
            parts = [p.strip() for p in cd.split(";")]
            filename_star = next((p.split("=", 1)[1] for p in parts if p.lower().startswith("filename*=")), None)
            if filename_star:
                # format: filename*=UTF-8''encoded-name
                val = filename_star.strip()
                if val.lower().startswith("utf-8''"):
                    import urllib.parse
                    return urllib.parse.unquote(val[7:])
                # generic fallback without encoding marker
                return val.strip('"').strip("'")
            filename = next((p.split("=", 1)[1] for p in parts if p.lower().startswith("filename=")), None)
            if filename:
                return filename.strip('"').strip("'")
        except Exception:
            return None
        return None

    def _get_int_env(self, key: str, default: int) -> int:
        import os
        try:
            val = os.getenv(key)
            return int(val) if val is not None else default
        except Exception:
            return default

    def _get_bool_env(self, key: str, default: bool) -> bool:
        import os
        val = os.getenv(key)
        if val is None:
            return default
        return val.strip().lower() in {"1", "true", "yes", "on"}
    
    async def download_file_by_id(self, request_id: str, file_id: str) -> bytes:
        """
        Download a generated file by its file ID using the API's file endpoint.
        Returns raw bytes.
        """
        endpoint = API_ENDPOINTS["get_file"].format(
            request_id=request_id,
            file_id=file_id,
        )
        response = await self._make_request("GET", endpoint)
        return response.content

    async def download_file_by_url(self, url: str) -> bytes:
        """
        Download a generated file directly from a provided URL.
        Returns raw bytes. Uses binary-safe buffering.
        """
        # Use the underlying AsyncClient to leverage shared settings
        resp = await self.client.get(url, headers=self.headers)
        if resp.status_code >= 400:
            self._handle_error_response(resp)
        # Ensure bytes are returned without decoding; httpx already provides bytes
        return resp.content

    async def wait_for_completion(
        self,
        request_id: str,
        poll_interval: Optional[float] = None,
        max_attempts: Optional[int] = None,
    ) -> StatusResponse:
        """
        Poll status until request completes.
        
        Args:
            request_id: The request ID to monitor.
            poll_interval: Seconds between polls (uses config default if None).
            max_attempts: Maximum polling attempts (uses config default if None).
        
        Returns:
            Final StatusResponse when complete.
        
        Raises:
            ProcessingError: If request fails or times out.
        """
        poll_interval = poll_interval or self.settings.poll_interval_seconds
        max_attempts = max_attempts or self.settings.max_poll_attempts
        
        attempts = 0
        delay = poll_interval
        
        while attempts < max_attempts:
            # Check status
            status = await self.get_status(request_id)
            
            # Log detailed status
            logger.debug(f"Polling attempt {attempts + 1}: status={status.status.value}, files_ready={status.files_ready}")
            
            # Check if terminal state
            if status.status in {RequestStatus.COMPLETED, RequestStatus.FAILED, RequestStatus.EXPIRED}:
                if status.status == RequestStatus.FAILED:
                    raise ProcessingError(
                        f"Visual generation failed: {status.error or 'Unknown error'}"
                    )
                elif status.status == RequestStatus.EXPIRED:
                    raise ProcessingError("Request expired")
                return status
            
            # Log progress
            if status.progress:
                logger.info(f"Progress: {status.progress:.0f}% - {status.message or ''}")
            
            # Wait with exponential backoff
            await asyncio.sleep(delay)
            delay = min(delay * 1.2, 30)  # Cap at 30 seconds
            attempts += 1
        
        raise ProcessingError(f"Timeout after {max_attempts} attempts")
    
    def get_rate_limit_status(self) -> Optional[RateLimitInfo]:
        """
        Get current rate limit status.
        
        Returns:
            RateLimitInfo if available, None otherwise.
        """
        return self.rate_limit_info
