# Napkin AI Introduction & Styles Guide

Executive Overview
This document introduces the Napkin API concepts and style catalog used by the Napkin AI API Playground. It complements docs/API_REFERENCE.md and focuses on style selection and API workflow basics.

About Napkin
Napkin is an AI-powered visual creation platform that turns text into engaging visuals. The API enables programmatic creation of diagrams and illustrations at scale.

🔒 Developer Preview
Access is invite-only. Request tokens at api@napkin.ai.

Token Usage
Include your token with every request:
```
Authorization: Bearer YOUR_TOKEN_HERE
```

## Key Features

- 🎨 **Multiple Visual Styles:** Choose from 15 built-in professional styles or create custom styles to match your brand
- 🌍 **Multi-language Support:** Generate visuals in any language using BCP 47 language tags
- 📐 **Flexible Formats:** Export as scalable SVG or raster PNG with custom dimensions
- 🔄 **Variation Generation:** Create up to 4 unique visual variations per request
- 🎯 **Context-aware:** Add context before and after your main content for more meaningful visuals
- ⚡ **Fast Processing:** Asynchronous processing with status polling for optimal performance
- 🔧 **Customization Options:** Transparent backgrounds, color inversion, and dimension control

## Getting Your API Token

To use the Napkin API, you need an API token.

**Request yours by emailing:** api@napkin.ai

Once you receive your token, include it in all requests using the Authorization header:

```
Authorization: Bearer YOUR_TOKEN_HERE
```

## Rate Limits & Version Info

Rate Limits
- 60 requests/minute per token (subject to change by provider)
- Headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, Retry-After
- Back off on 429; see API reference for retry guidance

API Version
- Current public API version path used by this client: v1
- Treat version headers as informational; pin base URL/version via environment where needed

## Available Visual Styles

Choose from a comprehensive collection of visual styles to match your content and brand. Each style has a unique ID that you'll need to pass as the `style_id` parameter in your API requests.

### 🎨 Colorful Styles
Vibrant and energetic designs for bold presentations:

| Style Name | Description | Style ID |
|------------|-------------|----------|
| Vibrant Strokes | A flow of vivid lines for bold notes | `CDQPRVVJCSTPRBBCD5Q6AWR` |
| Glowful Breeze | A swirl of cheerful color for laid-back planning | `CDQPRVVJCSTPRBBKDXK78` |
| Bold Canvas | A vivid field of shapes for lively notes | `CDQPRVVJCSTPRBB6DHGQ8` |
| Radiant Blocks | A bright spread of solid color for tasks | `CDQPRVVJCSTPRBB6D5P6RSB4` |
| Pragmatic Shades | A palette of blended hues for bold ideas | `CDQPRVVJCSTPRBB7E9GP8TB5DST0` |

### 😊 Casual Styles
Relaxed and approachable visuals for informal content:

| Style Name | Description | Style ID |
|------------|-------------|----------|
| Carefree Mist | A wisp of calm tones for playful tasks | `CDGQ6XB1DGPQ6VV6EG` |
| Lively Layers | A breeze of soft color for bright ideas | `CDGQ6XB1DGPPCTBCDHJP8` |

### ✏️ Hand-drawn Styles
Artistic, sketch-like appearance for creative projects:

| Style Name | Description | Style ID |
|------------|-------------|----------|
| Artistic Flair | A splash of hand-drawn color for creative thinking | `D1GPWS1DCDQPRVVJCSTPR` |
| Sketch Notes | A hand-drawn style for free-flowing ideas | `D1GPWS1DDHMPWSBK` |

### 💼 Formal Styles
Professional and clean designs for business use:

| Style Name | Description | Style ID |
|------------|-------------|----------|
| Elegant Outline | A refined black outline for professional clarity | `CSQQ4VB1DGPP4V31CDNJTVKFBXK6JV3C` |
| Subtle Accent | A light touch of color for professional documents | `CSQQ4VB1DGPPRTB7D1T0` |
| Monochrome Pro | A single-color approach for focused presentations | `CSQQ4VB1DGPQ6TBECXP6ABB3DXP6YWG` |
| Corporate Clean | A professional flat style for business diagrams | `CSQQ4VB1DGPPTVVEDXHPGWKFDNJJTSKCC5T0` |

### ⚫ Monochrome Styles
Minimalist black, white, and gray aesthetics:

| Style Name | Description | Style ID |
|------------|-------------|----------|
| Minimal Contrast | A clean monochrome style for focused work | `DNQPWVV3D1S6YVB55NK6RRBM` |
| Silver Beam | A spotlight of gray scale ease with striking focus | `CXS62Y9DCSQP6XBK` |

### 🎨 Custom Styles
Create personalized styles that perfectly match your brand:

#### How to Create Custom Styles
1. **Visit Napkin:** Go to app.napkin.ai
2. **Create Custom Style:** Use the style editor to create a custom style that matches your brand
3. **Copy Style ID:** Once your custom style is created, copy its unique ID
4. **Use in API:** Pass the custom style ID as the `style_id` parameter in your API requests

⚠️ **Important Note:** Custom fonts added in custom styles are not yet supported in the API. Please use standard web fonts for now.

### Usage Example with Styles

```python
import requests

# Using a built-in style (Vibrant Strokes)
data = {
    "format": "svg",
    "content": "Your amazing content here",
    "style_id": "CDQPRVVJCSTPRBBCD5Q6AWR",  # Vibrant Strokes style
    "number_of_visuals": 2
}

response = requests.post(
    "https://api.napkin.ai/v1/visual",
    headers={
        "Authorization": "Bearer YOUR_TOKEN",
        "Content-Type": "application/json"
    },
    json=data
)
```

## Error Handling Overview

The API returns standard HTTP status codes to help you handle errors appropriately:

| Status Code | Description | Action Required |
|-------------|-------------|-----------------|
| 201 | Visual request created successfully | Continue to poll status |
| 400 | Invalid request data | Check request parameters |
| 401 | Authentication required or invalid token | Verify your API token |
| 403 | Access denied to resource | Check resource ownership |
| 404 | Resource not found | Verify request/file IDs |
| 410 | Request has expired | Create a new request |
| 429 | Rate limit exceeded | Wait and retry with backoff |
| 500 | Internal server error | Retry request or contact support |

## Best Practices

### 1. Implement Exponential Backoff
When polling for status, increase the interval between requests to reduce API load:

```javascript
// Helper wait function
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

let delay = 2000; // Start with 2 seconds
const maxDelay = 30000; // Max 30 seconds
const maxAttempts = 30; // Prevent infinite loops
let attempts = 0;

while (status === 'pending' && attempts < maxAttempts) {
  await wait(delay);
  // Check status...
  delay = Math.min(Math.round(delay * 1.5), maxDelay); // Exponential backoff
  attempts++;
}
```

### 2. Handle Rate Limits
Respect the rate limit headers and implement retry logic:

```python
import time

if response.status_code == 429:
    retry_after = int(response.headers.get('Retry-After', '60'))
    time.sleep(retry_after)
    # Retry request
```

```javascript
// Never expose tokens in client-side browser code. Use server-side only.
if (response.status === 429) {
  const retryAfter = parseInt(response.headers.get('Retry-After') || '60', 10);
  await new Promise((r) => setTimeout(r, retryAfter * 1000));
  // Retry request
}
```

### 3. Cache Results
Store generated visuals to avoid redundant API calls for the same content.

### 4. Use Appropriate Formats
- Choose SVG for scalability and smaller file sizes
- Choose PNG when you need specific pixel dimensions or raster format

### 5. Provide Context
Use `context_before` and `context_after` for better visual generation:

```json
{
  "content": "Machine Learning",
  "context_before": "Introduction to",
  "context_after": "for beginners"
}
```

### 6. Language Tags
Always specify the correct language for optimal results:

```json
{
  "content": "Bonjour le monde",
  "language": "fr-FR"
}
```

## Support & Resources

- **Documentation Issues:** Report to api@napkin.ai
- **API Access:** Request tokens at api@napkin.ai
- **Technical Support:** Include your request ID when reporting issues
- **Main Website:** napkin.ai
- **Web App:** app.napkin.ai

## Quick Links

- [API Documentation](#napkin-ai-api-documentation)
- [Create Visual Request](#1-create-visual-request)
- [Get Visual Request Status](#2-get-visual-request-status)
- [Download Generated File](#3-download-generated-file)

Ready to start creating amazing visuals? Get your API token and begin transforming your text into beautiful, professional graphics!

---

# Napkin AI API Documentation

**Note:** This is the first developer preview of the Napkin API. Please report any issues to api@napkin.ai.

## Base URL
```
https://api.napkin.ai
```

Authentication
Use a Bearer token:
```
Authorization: Bearer <token>
```

Endpoints

1) Create Visual Request
Creates a new visual content generation request (asynchronous).

Endpoint: POST /v1/visual

**Headers:**
```
Content-Type: application/json
Accept: application/json
Authorization: Bearer <token>
```

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `format` | string | Required | Output file format. Possible values: `svg`, `png` |
| `content` | string | Required | Main text content to visualize (non-empty) |
| `context_before` | string\|null | Optional | Text context that appears before the main content |
| `context_after` | string\|null | Optional | Text context that appears after the main content |
| `language` | string | Optional | BCP 47 language tag (e.g., `en`, `en-US`, `fr-FR`, `es-ES`, `de-DE`, `ja-JP`) |
| `style_id` | string\|null | Optional | Style identifier. See available styles for all options |
| `visual_id` | string | Optional | Single visual ID to regenerate with new content. Cannot be used with `number_of_visuals > 1` or with `visual_ids`, `visual_query`, or `visual_queries` |
| `visual_ids` | string[] | Optional | Array of visual IDs to regenerate. Must match `number_of_visuals`. Cannot be used with `visual_id`, `visual_query`, or `visual_queries` |
| `visual_query` | string | Optional | Query to search for visual type (e.g., "mindmap", "flowchart", "timeline"). Cannot be used with `number_of_visuals > 1` or with other visual parameters |
| `visual_queries` | string[] | Optional | Array of queries for visual types. Must match `number_of_visuals`. Cannot be used with other visual parameters |
| `number_of_visuals` | integer | Optional | Number of variations to generate (1-4). Default: 1 |
| `transparent_background` | boolean | Optional | Use transparent background. Default: false |
| `inverted_color` | boolean | Optional | Invert colors. Default: false |
| `width` | integer\|null | Optional | Width in pixels (100-10000). For PNG only. If both width and height set, width takes precedence |
| `height` | integer\|null | Optional | Height in pixels (100-10000). For PNG only. Ignored if width is set |

#### Visual Selection Options

Visual Selection Options (mutually exclusive)
- New visuals: omit selection parameters
- Regenerate one: visual_id (number_of_visuals must be 1 or unset)
- Regenerate many: visual_ids (length equals number_of_visuals)
- Search one type: visual_query (e.g., "mindmap", "timeline")
- Search multiple types: visual_queries (length equals number_of_visuals)

Validation examples (400 Bad Request):

```json
{
  "error": "invalid_parameters",
  "message": "visual_id cannot be combined with number_of_visuals > 1, visual_ids, visual_query, or visual_queries"
}
```

```json
{
  "error": "invalid_parameters",
  "message": "Length of visual_ids (3) must match number_of_visuals (2)"
}
```

#### Request Examples

**Basic Request:**
```json
{
  "format": "svg",
  "content": "Napkin API"
}
```

**Advanced Request with Style and Context:**
```json
{
  "format": "png",
  "content": "Napkin API",
  "context_before": "Welcome to",
  "context_after": "Generate beautiful visuals",
  "language": "en-US",
  "style_id": "CDQPRVVJCSTPRBBCD5Q6AWR",
  "number_of_visuals": 2,
  "transparent_background": true,
  "width": 1200
}
```

**Regenerate Existing Visual:**
```json
{
  "format": "svg",
  "content": "Updated content",
  "visual_id": "5UCQJLAV5S6NXEWS2PBJF54UYPW5NZ4G"
}
```

**Search for Visual Type:**
```json
{
  "format": "png",
  "content": "Project Timeline",
  "visual_query": "timeline",
  "width": 1600
}
```

#### Response

**Status Codes:**

| Code | Description |
|------|-------------|
| 201 | Visual request created successfully |
| 400 | Invalid request data |
| 401 | Authentication required or invalid token |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

**Success Response (201):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "pending",
  "request": {
    // Original request parameters
  },
  "generated_files": [
    // Array of generated file objects (when status is "completed")
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string (UUID) | Unique identifier of the request |
| `status` | string | Processing status: `pending`, `completed`, or `failed` |
| `request` | object | Original request parameters |
| `generated_files` | array | Array of generated file objects (populated when completed) |

#### CURL Example

```bash
curl -L 'https://api.napkin.ai/v1/visual' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer <token>' \
  -d '{
    "format": "svg",
    "content": "Napkin API",
    "context_before": "Welcome to",
    "context_after": "Generate beautiful visuals",
    "language": "en-US",
    "style_id": "CDQPRVVJCSTPRBBCD5Q6AWR",
    "number_of_visuals": 1,
    "transparent_background": true,
    "inverted_color": false,
    "width": 1200
  }'
```

#### Code Examples

**Python:**
```python
import requests
import json

url = "https://api.napkin.ai/v1/visual"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer YOUR_TOKEN"
}

data = {
    "format": "svg",
    "content": "Napkin API",
    "context_before": "Welcome to",
    "context_after": "Generate beautiful visuals",
    "language": "en-US",
    "style_id": "CDQPRVVJCSTPRBBCD5Q6AWR",
    "number_of_visuals": 1,
    "transparent_background": True
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(f"Request ID: {result['id']}")
print(f"Status: {result['status']}")
```

**JavaScript/Node.js:**
```javascript
const response = await fetch('https://api.napkin.ai/v1/visual', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer YOUR_TOKEN'
  },
  body: JSON.stringify({
    format: 'svg',
    content: 'Napkin API',
    context_before: 'Welcome to',
    context_after: 'Generate beautiful visuals',
    language: 'en-US',
    style_id: 'CDQPRVVJCSTPRBBCD5Q6AWR',
    number_of_visuals: 1,
    transparent_background: true
  })
});

const result = await response.json();
console.log(`Request ID: ${result.id}`);
console.log(`Status: ${result.status}`);
```

**Go:**
```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
)

func main() {
    url := "https://api.napkin.ai/v1/visual"
    
    payload := map[string]interface{}{
        "format": "svg",
        "content": "Napkin API",
        "context_before": "Welcome to",
        "context_after": "Generate beautiful visuals",
        "language": "en-US",
        "style_id": "CDQPRVVJCSTPRBBCD5Q6AWR",
        "number_of_visuals": 1,
        "transparent_background": true,
    }
    
    jsonData, _ := json.Marshal(payload)
    
    req, _ := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("Accept", "application/json")
    req.Header.Set("Authorization", "Bearer YOUR_TOKEN")
    
    client := &http.Client{}
    resp, _ := client.Do(req)
    defer resp.Body.Close()
    
    var result map[string]interface{}
    json.NewDecoder(resp.Body).Decode(&result)
    
    fmt.Printf("Request ID: %s\n", result["id"])
    fmt.Printf("Status: %s\n", result["status"])
}
```

2) Get Visual Request Status
Retrieve the current status and details of a visual request.

Endpoint: GET /v1/visual/:request-id/status

**Headers:**
```
Accept: application/json
Authorization: Bearer <token>
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `request-id` | string (UUID) | Required | The unique identifier of the visual request |

Example: `123e4567-e89b-12d3-a456-426614174000`

#### Response

**Status Codes:**

| Code | Description |
|------|-------------|
| 200 | Request status retrieved successfully |
| 400 | Invalid request ID format |
| 401 | Authentication required or invalid token |
| 403 | Access denied - request belongs to another user |
| 404 | Request not found |
| 410 | Request has expired and is no longer available |
| 500 | Internal server error |

**Response Body:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "completed",
  "request": {
    // Original request parameters
  },
  "generated_files": [
    // Array of generated file objects (when status is "completed")
  ]
}
```

**Status Values:**
- `pending`: Request is queued for processing
- `completed`: Processing finished successfully, files are available
- `failed`: Processing failed due to an error

When status is "completed", the response includes a `generated_files` array with download links and metadata.

⚠️ **Important:** Both status and file URLs expire after 30 minutes from generation.

#### CURL Example

```bash
curl -L 'https://api.napkin.ai/v1/visual/123e4567-e89b-12d3-a456-426614174000/status' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

#### Code Examples

**Python:**
```python
import requests

request_id = "123e4567-e89b-12d3-a456-426614174000"
url = f"https://api.napkin.ai/v1/visual/{request_id}/status"
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer YOUR_TOKEN"
}

response = requests.get(url, headers=headers)
result = response.json()

print(f"Status: {result['status']}")
if result['status'] == 'completed':
    print(f"Files available: {len(result['generated_files'])}")
```

**JavaScript/Node.js:**
```javascript
const requestId = "123e4567-e89b-12d3-a456-426614174000";
const response = await fetch(`https://api.napkin.ai/v1/visual/${requestId}/status`, {
  headers: {
    'Accept': 'application/json',
    'Authorization': 'Bearer YOUR_TOKEN'
  }
});

const result = await response.json();
console.log(`Status: ${result.status}`);

if (result.status === 'completed') {
  console.log(`Files available: ${result.generated_files.length}`);
}
```

3) Download Generated File
Download a specific file generated by a completed visual request.

Endpoint: GET /v1/visual/:request-id/file/:file-id

**Headers:**
```
Accept: image/svg+xml (or appropriate MIME type)
Authorization: Bearer <token>
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `request-id` | string (UUID) | Required | The unique identifier of the visual request |
| `file-id` | string | Required | The unique identifier of the file to download |

Example: `/v1/visual/123e4567-e89b-12d3-a456-426614174000/file/426614174000-wdjvjhwv8`

#### Important Notes

- **URL provided automatically:** The complete download URL is provided in the `generated_files` array from the status endpoint - you don't need to construct it manually
- **Authentication required:** Authentication headers are required to download the file content
- **Host files elsewhere:** Files should be downloaded and hosted elsewhere for display purposes - do not use these URLs directly for displaying visuals in your application
- **30-minute expiration:** Both status and file URLs expire after 30 minutes from generation
- **Availability:** Files are only available for requests with status "completed"

#### Response

**Status Codes:**

| Code | Description |
|------|-------------|
| 200 | File downloaded successfully |
| 400 | Invalid request ID or file ID format |
| 401 | Authentication required or invalid token |
| 403 | Access denied - request belongs to another user |
| 404 | Request or file not found |
| 410 | Request has expired and is no longer available |
| 500 | Internal server error |

**Response Headers (200):**

| Header | Description | Example |
|--------|-------------|---------|
| Content-Type | MIME type of the file | `image/svg+xml`, `image/png` |
| Content-Length | Size of the file in bytes | `245760` |

**Response Body:**
Binary file content (SVG or PNG)

#### CURL Example

```bash
curl -L 'https://api.napkin.ai/v1/visual/123e4567-e89b-12d3-a456-426614174000/file/426614174000-wdjvjhwv8' \
  -H 'Accept: image/svg+xml' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  --output visual.svg
```

#### Code Examples

**Python:**
```python
import requests

request_id = "123e4567-e89b-12d3-a456-426614174000"
file_id = "426614174000-wdjvjhwv8"
url = f"https://api.napkin.ai/v1/visual/{request_id}/file/{file_id}"
headers = {
    "Accept": "image/svg+xml",  # or "image/png" depending on format
    "Authorization": "Bearer YOUR_TOKEN"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Save the file
    with open("visual.svg", "wb") as f:
        f.write(response.content)
    print("File downloaded successfully")
else:
    print(f"Error: {response.status_code}")
```

**JavaScript/Node.js:**
```javascript
const fs = require('fs');
const fetch = require('node-fetch');

const requestId = "123e4567-e89b-12d3-a456-426614174000";
const fileId = "426614174000-wdjvjhwv8";
const url = `https://api.napkin.ai/v1/visual/${requestId}/file/${fileId}`;

const response = await fetch(url, {
  headers: {
    'Accept': 'image/svg+xml',
    'Authorization': 'Bearer YOUR_TOKEN'
  }
});

if (response.ok) {
  const buffer = await response.buffer();
  fs.writeFileSync('visual.svg', buffer);
  console.log('File downloaded successfully');
} else {
  console.error(`Error: ${response.status}`);
}
```

#### Using with Status Endpoint

The typical flow is to get the download URLs from the status endpoint:

```javascript
// 1. Get status and file URLs
const statusResponse = await fetch(`https://api.napkin.ai/v1/visual/${requestId}/status`, {
  headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
});

const statusData = await statusResponse.json();

if (statusData.status === 'completed') {
  // 2. Download each generated file
  for (const file of statusData.generated_files) {
    // The file object contains the complete download URL
    const downloadResponse = await fetch(file.url, {
      headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
    });
    
    if (downloadResponse.ok) {
      const fileContent = await downloadResponse.buffer();
      // Save or process the file
      fs.writeFileSync(`visual_${file.id}.${file.format}`, fileContent);
    }
  }
}
```

⚠️ **Best Practice:** Download files immediately after generation and host them on your own infrastructure. Do not use the API URLs directly in your application as they expire after 30 minutes.

## Security Notes

- Do not embed API tokens in client-side/browser code or static frontends. Keep tokens on the server.
- Prefer server-to-server requests; if using a web app, proxy requests through your backend.
- Rotate tokens regularly and store them securely (environment variables or secret managers).

## Workflow Overview

Typical workflow:
1) POST /v1/visual with content and options
2) Poll GET /v1/visual/:id/status every 2–3s with exponential backoff
3) Download files via the provided URLs (Authorization required)
4) Host files on your infrastructure; API URLs expire after ~30 minutes

### Complete Workflow Example

```javascript
// 1. Create visual request
const createResponse = await fetch('https://api.napkin.ai/v1/visual', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_TOKEN'
  },
  body: JSON.stringify({
    format: 'svg',
    content: 'Your content here',
    number_of_visuals: 2
  })
});

const { id } = await createResponse.json();
console.log(`Request created: ${id}`);

// 2. Poll for status
let status = 'pending';
let result;
const maxAttempts = 30; // Max 90 seconds polling
let attempts = 0;

while (status === 'pending' && attempts < maxAttempts) {
  const statusResponse = await fetch(`https://api.napkin.ai/v1/visual/${id}/status`, {
    headers: {
      'Authorization': 'Bearer YOUR_TOKEN'
    }
  });
  
  result = await statusResponse.json();
  status = result.status;
  
  if (status === 'pending') {
    await new Promise(resolve => setTimeout(resolve, 3000)); // Wait 3 seconds
    attempts++;
  }
}

// 3. Handle result
if (status === 'completed') {
  console.log(`Success! ${result.generated_files.length} files generated`);
  // Download files using the URLs in result.generated_files
  // Remember: URLs expire after 30 minutes!
} else if (status === 'failed') {
  console.error('Visual generation failed');
} else {
  console.error('Timeout waiting for visual generation');
}
```

## Important Notes

- Requests are asynchronous; typical latency 5–15s, depending on complexity
- Status and file URLs expire (~30 minutes); download promptly
- Outputs: SVG or PNG; dimensions apply to PNG only (SVG scales)
- Regeneration and visual type search are supported via visual_id/visual_query
- Rate limiting applies; observe Retry-After
- Security: do not expose tokens in browser code; prefer server-to-server calls

## Support

For API issues or questions, contact: **api@napkin.ai**