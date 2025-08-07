# Napkin AI API Guide

## Getting Started

### Prerequisites
- Python 3.10+
- Napkin API token (request at api@napkin.ai)

### Installation

```bash
# Clone repository
git clone https://github.com/moshehbenavraham/Napkin-AI-API.git
cd Napkin-AI-API

# Install dependencies
poetry install

# Configure API token
cp .env.example .env
echo "NAPKIN_API_TOKEN=your_token_here" >> .env
```

## Usage

### Web Interface (Streamlit)

```bash
poetry run streamlit run streamlit_app.py
# Access at http://localhost:8501
```

Features:
- Interactive visual generation
- 16 built-in styles + custom styles
- 38 language support
- Real-time preview and download

### Command Line Interface

```bash
# Basic generation
poetry run napkin generate "Your content"

# With options
poetry run napkin generate "Data Flow" \
  --style sketch-notes \
  --format png \
  --language es-ES \
  --variations 2

# List available styles
poetry run napkin styles --list

# Check configuration
poetry run napkin config --check
```

## API Reference

### Base Configuration

- **Base URL**: `https://api.napkin.ai`
- **Version**: `v1`
- **Authentication**: Bearer token required
- **Rate Limit**: 60 requests/minute

### Core Endpoints

#### 1. Create Visual Request

**POST** `/v1/visual`

```python
import httpx
import asyncio

data = {
    "format": "svg",  # or "png"
    "content": "Your text content",
    "style_id": "CDQPRVVJCSTPRBBCD5Q6AWR",  # Optional
    "language": "en-US",  # BCP 47 tag
    "number_of_visuals": 1,  # 1-4
    "transparent_background": False,
    "width": 1200,  # PNG only
    "context_before": "Introduction to",
    "context_after": "for beginners"
}

async def create_visual():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.napkin.ai/v1/visual",
            headers={"Authorization": "Bearer YOUR_TOKEN"},
            json=data
        )
        return response.json()

result = asyncio.run(create_visual())
print(f"Request ID: {result['id']}")
```

#### 2. Check Status

**GET** `/v1/visual/{request_id}/status`

```python
async def check_status(request_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.napkin.ai/v1/visual/{request_id}/status",
            headers={"Authorization": "Bearer YOUR_TOKEN"}
        )
        return response.json()

# Poll until complete
status = "pending"
while status == "pending":
    result = asyncio.run(check_status(request_id))
    status = result["status"]
    if status == "pending":
        await asyncio.sleep(3)
```

#### 3. Download File

**GET** `/v1/visual/{request_id}/file/{file_id}`

```python
async def download_file(request_id, file_id, output_path):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.napkin.ai/v1/visual/{request_id}/file/{file_id}",
            headers={"Authorization": "Bearer YOUR_TOKEN"}
        )
        with open(output_path, "wb") as f:
            f.write(response.content)
```

## Available Styles

### Colorful Styles
| Style | ID | Description |
|-------|----|--------------|
| Vibrant Strokes | `CDQPRVVJCSTPRBBCD5Q6AWR` | Bold, vivid lines |
| Glowful Breeze | `CDQPRVVJCSTPRBBKDXK78` | Cheerful colors |
| Bold Canvas | `CDQPRVVJCSTPRBB6DHGQ8` | Lively shapes |
| Radiant Blocks | `CDQPRVVJCSTPRBB6D5P6RSB4` | Solid colors |
| Pragmatic Shades | `CDQPRVVJCSTPRBB7E9GP8TB5DST0` | Blended hues |

### Hand-drawn Styles
| Style | ID | Description |
|-------|----|--------------|
| Artistic Flair | `D1GPWS1DCDQPRVVJCSTPR` | Creative hand-drawn |
| Sketch Notes | `D1GPWS1DDHMPWSBK` | Free-flowing sketches |

### Formal Styles
| Style | ID | Description |
|-------|----|--------------|
| Elegant Outline | `CSQQ4VB1DGPP4V31CDNJTVKFBXK6JV3C` | Professional clarity |
| Subtle Accent | `CSQQ4VB1DGPPRTB7D1T0` | Light professional |
| Corporate Clean | `CSQQ4VB1DGPPTVVEDXHPGWKFDNJJTSKCC5T0` | Business diagrams |

### Casual & Monochrome
| Style | ID | Description |
|-------|----|--------------|
| Carefree Mist | `CDGQ6XB1DGPQ6VV6EG` | Playful tasks |
| Lively Layers | `CDGQ6XB1DGPPCTBCDHJP8` | Soft colors |
| Minimal Contrast | `DNQPWVV3D1S6YVB55NK6RRBM` | Clean monochrome |
| Silver Beam | `CXS62Y9DCSQP6XBK` | Grayscale focus |

## Error Handling

| Status Code | Description | Action |
|-------------|-------------|--------|
| 201 | Request created | Poll for status |
| 400 | Invalid parameters | Check request data |
| 401 | Invalid token | Verify API token |
| 429 | Rate limit exceeded | Wait and retry |
| 410 | Request expired | Create new request |

## Best Practices

1. **Implement exponential backoff** when polling
2. **Cache generated visuals** to avoid redundant API calls
3. **Download files immediately** (URLs expire after 30 minutes)
4. **Use SVG format** for scalability, PNG for specific dimensions
5. **Add context** for better visual generation
6. **Specify language** for non-English content

## Security

- Never expose API tokens in client-side code
- Use environment variables for sensitive data
- Implement server-side proxy for web applications
- Rotate tokens regularly

## Support

- **API Issues**: api@napkin.ai
- **GitHub Issues**: [Project Issues](https://github.com/moshehbenavraham/Napkin-AI-API/issues)
- **Documentation**: [Official API Docs](docs/napkin_official/NAPKIN_AI_API.md)