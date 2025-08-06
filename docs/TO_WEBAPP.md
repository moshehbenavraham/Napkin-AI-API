# Web App Migration Plan

## Overview

Transform the Napkin AI API CLI into a web application using the **simplest, most cost-effective approach** with GitHub integration.

## Recommended Approach: Streamlit Cloud

### Why Streamlit?
- **100% Free** - No costs for hosting, deployment, or usage
- **5-Minute Setup** - Literally just create one Python file
- **Zero Infrastructure** - No servers, databases, or DevOps needed
- **Uses Existing Code** - Import your modules directly, no API rewrite
- **GitHub Integration** - Auto-deploys from your repo
- **Built-in Features** - File uploads, downloads, async support, progress bars

### Implementation Plan

#### Step 1: Create Streamlit App (15 minutes)

Create `webapp.py` in project root:

```python
import streamlit as st
import asyncio
from src.core.generator import VisualGenerator
from src.utils.constants import STYLES
from src.utils.config import Settings

st.set_page_config(
    page_title="Napkin AI Visual Generator",
    page_icon="<¨",
    layout="wide"
)

st.title("<¨ Napkin AI Visual Generator")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    
    # API token from Streamlit secrets
    api_token = st.secrets.get("NAPKIN_API_TOKEN", "")
    if not api_token:
        st.error("Please configure API token in Streamlit secrets")
    
    # Style selector
    style_category = st.selectbox(
        "Style Category",
        options=list(set(s["category"] for s in STYLES.values()))
    )
    
    filtered_styles = {k: v for k, v in STYLES.items() 
                       if v["category"] == style_category}
    
    selected_style = st.selectbox(
        "Visual Style",
        options=list(filtered_styles.keys()),
        format_func=lambda x: filtered_styles[x]["name"]
    )
    
    # Format options
    format_type = st.radio("Format", ["svg", "png"])
    
    if format_type == "png":
        width = st.slider("Width", 100, 4096, 1920)
        height = st.slider("Height", 100, 4096, 1080)
    else:
        width = height = None
    
    variations = st.slider("Variations", 1, 4, 1)

# Main content area
content = st.text_area(
    "Enter your content to visualize:",
    height=150,
    placeholder="Describe what you want to visualize..."
)

if st.button("=€ Generate Visual", type="primary"):
    if not content:
        st.error("Please enter some content")
    elif not api_token:
        st.error("API token not configured")
    else:
        with st.spinner("Generating visual..."):
            # Run async generator
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
                result = asyncio.run(generate())
                
                st.success(f"Generated {len(result.files)} visual(s)!")
                
                # Display results
                cols = st.columns(variations)
                for idx, file_url in enumerate(result.files):
                    with cols[idx % variations]:
                        st.image(file_url, use_column_width=True)
                        
                        # Download button
                        file_name = f"napkin_{selected_style}_{idx+1}.{format_type}"
                        st.download_button(
                            label=f"Download {file_name}",
                            data=requests.get(file_url).content,
                            file_name=file_name,
                            mime=f"image/{format_type}"
                        )
                        
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Powered by [Napkin AI](https://napkin.ai)")
```

#### Step 2: Add Requirements (2 minutes)

Create `requirements-webapp.txt`:
```txt
streamlit>=1.29.0
-r requirements.txt
```

#### Step 3: Configure Streamlit Secrets (3 minutes)

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

Create `.streamlit/secrets.toml` (local testing only, don't commit):
```toml
NAPKIN_API_TOKEN = "your-api-token-here"
```

#### Step 4: Deploy to Streamlit Cloud (5 minutes)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Connect your GitHub repo
5. Set main file path: `webapp.py`
6. Add secret in Advanced Settings: `NAPKIN_API_TOKEN`
7. Deploy!

Your app will be live at: `https://yourapp.streamlit.app`

### Total Setup Time: ~25 minutes

## Alternative: GitHub Pages + Vercel API

If you prefer a more traditional web architecture:

### Frontend (GitHub Pages - Free)

Create `docs/index.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Napkin AI Generator</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto p-8">
        <h1 class="text-3xl font-bold mb-8">Napkin AI Visual Generator</h1>
        
        <div class="bg-white p-6 rounded-lg shadow">
            <textarea id="content" class="w-full p-3 border rounded" 
                      placeholder="Enter content..."></textarea>
            
            <select id="style" class="mt-4 p-2 border rounded">
                <!-- Populate with styles -->
            </select>
            
            <button onclick="generate()" 
                    class="mt-4 bg-blue-500 text-white px-6 py-2 rounded">
                Generate
            </button>
            
            <div id="results" class="mt-8"></div>
        </div>
    </div>
    
    <script>
        const API_URL = 'https://your-api.vercel.app';
        
        async function generate() {
            const content = document.getElementById('content').value;
            const style = document.getElementById('style').value;
            
            const response = await fetch(`${API_URL}/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('apiToken')}`
                },
                body: JSON.stringify({ content, style })
            });
            
            const result = await response.json();
            displayResults(result);
        }
        
        function displayResults(result) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = result.files.map(url => 
                `<img src="${url}" class="mt-4 rounded shadow">`
            ).join('');
        }
    </script>
</body>
</html>
```

### Backend (Vercel - Free Tier)

Create `api/generate.py`:
```python
from http.server import BaseHTTPRequestHandler
import json
import asyncio
from src.core.generator import VisualGenerator
from src.utils.config import Settings

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Handle CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Parse request
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        # Generate visual
        settings = Settings(napkin_api_token=os.environ['NAPKIN_API_TOKEN'])
        result = asyncio.run(generate_visual(data, settings))
        
        # Return response
        self.wfile.write(json.dumps(result).encode())

async def generate_visual(data, settings):
    async with VisualGenerator(settings) as generator:
        result = await generator.generate(
            content=data['content'],
            style=data.get('style', 'vibrant-strokes')
        )
        return {'files': result.files}
```

Create `vercel.json`:
```json
{
  "functions": {
    "api/generate.py": {
      "runtime": "python3.9"
    }
  }
}
```

Deploy:
```bash
npm i -g vercel
vercel
```

## Comparison

| Approach | Setup Time | Cost | Complexity | Best For |
|----------|------------|------|------------|----------|
| **Streamlit** | 25 min | Free | P | Quick prototypes, Python devs |
| **GitHub Pages + Vercel** | 45 min | Free | PP | Custom UI, more control |
| **Flask on Render** | 30 min | Free tier | PP | Traditional web app |
| **FastAPI on Railway** | 40 min | $5/mo | PPP | Production API |

## Recommended: Streamlit

For your use case, **Streamlit is perfect** because:
1. You already have Python code that works
2. Zero learning curve - just Python
3. Completely free forever
4. Built-in file handling, async support
5. Professional-looking UI with no CSS/JS
6. Deploy in literally 5 minutes

## Next Steps

1. Choose Streamlit (recommended) or GitHub Pages approach
2. Create the web app file(s)
3. Test locally
4. Deploy to free hosting
5. Share your app URL!

## Quick Commands

### Streamlit Local Testing
```bash
pip install streamlit
streamlit run webapp.py
```

### GitHub Pages Deployment
```bash
# Enable GitHub Pages in repo settings
# Set source to /docs folder
# Your site will be at: https://username.github.io/Napkin-AI-API/
```

### Vercel Deployment
```bash
npm i -g vercel
vercel --prod
```

## Security Notes

- Never commit API tokens to GitHub
- Use environment variables or secrets management
- For Streamlit: Use st.secrets
- For Vercel: Use environment variables
- For GitHub Pages: Use a proxy or serverless function

## Total Time to Deploy: 25-45 minutes

The Streamlit approach can have you live in under 30 minutes with zero infrastructure costs!