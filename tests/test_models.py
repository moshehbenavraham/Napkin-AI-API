"""
Tests for API models.
"""

import pytest
from pydantic import ValidationError

from src.api.models import (
    VisualRequest,
    RequestStatus,
    OutputFormat,
    GeneratedFile,
    VisualResponse,
    StatusResponse,
    RateLimitInfo,
)


class TestVisualRequest:
    """Test VisualRequest model."""
    
    def test_valid_request(self):
        """Test creating a valid request."""
        request = VisualRequest(
            content="Test content",
            format=OutputFormat.SVG,
            style_id="test-style",
            language="en-US",
            number_of_visuals=2,
        )
        assert request.content == "Test content"
        assert request.format == OutputFormat.SVG
        assert request.number_of_visuals == 2
    
    def test_default_values(self):
        """Test default values are applied."""
        request = VisualRequest(content="Test")
        assert request.format == OutputFormat.SVG
        assert request.language == "en-US"
        assert request.number_of_visuals == 1
        assert request.transparent_background is False
        assert request.inverted_color is False
    
    def test_png_dimensions_validation(self):
        """Test PNG dimensions are only allowed for PNG format."""
        # Valid: PNG with dimensions
        request = VisualRequest(
            content="Test",
            format=OutputFormat.PNG,
            width=1024,
            height=768,
        )
        assert request.width == 1024
        assert request.height == 768
        
        # Invalid: SVG with dimensions
        with pytest.raises(ValidationError) as exc_info:
            VisualRequest(
                content="Test",
                format=OutputFormat.SVG,
                width=1024,
            )
        assert "Width and height can only be set for PNG format" in str(exc_info.value)
    
    def test_content_validation(self):
        """Test content length validation."""
        # Valid content
        request = VisualRequest(content="a" * 100)
        assert len(request.content) == 100
        
        # Empty content should fail
        with pytest.raises(ValidationError):
            VisualRequest(content="")
    
    def test_number_of_visuals_range(self):
        """Test number_of_visuals range validation."""
        # Valid range
        for n in [1, 2, 3, 4]:
            request = VisualRequest(content="Test", number_of_visuals=n)
            assert request.number_of_visuals == n
        
        # Invalid: too low
        with pytest.raises(ValidationError):
            VisualRequest(content="Test", number_of_visuals=0)
        
        # Invalid: too high
        with pytest.raises(ValidationError):
            VisualRequest(content="Test", number_of_visuals=5)


class TestVisualResponse:
    """Test VisualResponse model."""
    
    def test_status_properties(self):
        """Test status checking properties."""
        from datetime import datetime
        
        # Completed status
        response = VisualResponse(
            request_id="test-123",
            status=RequestStatus.COMPLETED,
            created_at=datetime.utcnow(),
        )
        assert response.is_completed is True
        assert response.is_failed is False
        assert response.is_expired is False
        assert response.is_terminal is True
        
        # Failed status
        response = VisualResponse(
            request_id="test-123",
            status=RequestStatus.FAILED,
            created_at=datetime.utcnow(),
            error="Test error",
        )
        assert response.is_completed is False
        assert response.is_failed is True
        assert response.is_terminal is True
        
        # Pending status
        response = VisualResponse(
            request_id="test-123",
            status=RequestStatus.PENDING,
            created_at=datetime.utcnow(),
        )
        assert response.is_terminal is False


class TestRateLimitInfo:
    """Test RateLimitInfo model."""
    
    def test_is_exceeded_property(self):
        """Test rate limit exceeded checking."""
        from datetime import datetime, timedelta
        
        # Not exceeded
        info = RateLimitInfo(
            limit=60,
            remaining=30,
            reset=datetime.utcnow() + timedelta(minutes=5),
        )
        assert info.is_exceeded is False
        
        # Exceeded
        info = RateLimitInfo(
            limit=60,
            remaining=0,
            reset=datetime.utcnow() + timedelta(minutes=5),
            retry_after=300,
        )
        assert info.is_exceeded is True


class TestStatusResponse:
    """Test StatusResponse model."""
    
    def test_progress_validation(self):
        """Test progress percentage validation."""
        # Valid progress
        status = StatusResponse(
            request_id="test-123",
            status=RequestStatus.PROCESSING,
            progress=50.0,
        )
        assert status.progress == 50.0
        
        # Progress at boundaries
        status = StatusResponse(
            request_id="test-123",
            status=RequestStatus.PROCESSING,
            progress=0.0,
        )
        assert status.progress == 0.0
        
        status = StatusResponse(
            request_id="test-123",
            status=RequestStatus.PROCESSING,
            progress=100.0,
        )
        assert status.progress == 100.0
        
        # Invalid: over 100
        with pytest.raises(ValidationError):
            StatusResponse(
                request_id="test-123",
                status=RequestStatus.PROCESSING,
                progress=101.0,
            )
        
        # Invalid: negative
        with pytest.raises(ValidationError):
            StatusResponse(
                request_id="test-123",
                status=RequestStatus.PROCESSING,
                progress=-1.0,
            )