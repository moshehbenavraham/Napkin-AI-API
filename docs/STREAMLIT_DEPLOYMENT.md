# Streamlit Cloud Deployment Guide

This guide covers deploying the Napkin AI Visual Generator web interface to Streamlit Cloud.

## Prerequisites

- GitHub account with repository access
- Napkin AI API token
- Python 3.10+ locally for testing

## Local Testing

Before deploying, test the app locally:

```bash
# Install dependencies
poetry install

# Set environment variable (optional, can use UI input)
export NAPKIN_API_TOKEN="your-token-here"

# Run the app
poetry run streamlit run streamlit_app.py

# Open in browser
# http://localhost:8501
```

## Deployment Steps

### 1. Prepare Your Repository

Ensure these files are in your repository:
- `streamlit_app.py` - Main application file
- `pyproject.toml` - Poetry dependencies (Streamlit Cloud supports Poetry)
- `.streamlit/config.toml` - App configuration

### 2. Create Streamlit Cloud Account

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign up with GitHub
3. Authorize Streamlit to access your repositories

### 3. Deploy Your App

1. Click **"New app"** in Streamlit Cloud dashboard
2. Select your repository and branch
3. Set **Main file path**: `streamlit_app.py`
4. Open **Advanced settings**

### 4. Configure Secrets

In Advanced settings, add your secrets in TOML format:

```toml
# Required
NAPKIN_API_TOKEN = "your-actual-napkin-api-token"

# Optional defaults
[defaults]
style = "vibrant-strokes"
format = "svg"
variations = 1
```

**Important**: Never commit secrets to your repository!

### 5. Python Version

In Advanced settings, set:
- **Python version**: `3.10`

### 6. Deploy

Click **Deploy!** Your app will be available at:
```
https://[your-app-name].streamlit.app
```

## Post-Deployment

### Viewing Logs

1. Go to your app in Streamlit Cloud dashboard
2. Click **"Manage app"**
3. Select **"Logs"** to view deployment and runtime logs

### Updating the App

The app auto-deploys when you push to the configured branch:

```bash
# Make changes locally
git add .
git commit -m "Update streamlit app"
git push origin main
```

### Monitoring

Check the footer of your deployed app for:
- Version number (currently v0.2.1)
- Git commit hash
- Last update timestamp

## Configuration

### Environment Variables

The app supports these environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `NAPKIN_API_TOKEN` | Your Napkin AI API token | Yes* |

*Can be entered via UI if not set in environment

### Custom Theme

Edit `.streamlit/config.toml` to customize appearance:

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

## Troubleshooting

### App Won't Start

1. Check Python version is 3.10+
2. Verify all dependencies in `pyproject.toml`
3. Check logs for import errors

### 403 Forbidden Errors

This was fixed in v0.2.1. The app now:
- Adds Bearer token authentication to API requests
- Pre-downloads files in worker thread
- Handles both CDN URLs and authenticated endpoints

### Memory Issues

If you encounter memory errors:
1. Reduce image dimensions (PNG)
2. Generate fewer variations
3. Use SVG format when possible

### Slow Generation

- Check Napkin AI service status
- Verify network connectivity
- Consider reducing variations

## Security Best Practices

1. **Never commit API tokens** to your repository
2. **Use Streamlit secrets** for sensitive data
3. **Rotate tokens regularly**
4. **Monitor usage** in your Napkin AI dashboard
5. **Set spending limits** if available

## Advanced Configuration

### Custom Domain

Streamlit Cloud supports custom domains (Pro plan):
1. Go to app settings
2. Add your domain
3. Configure DNS CNAME

### Analytics

Add analytics by modifying `streamlit_app.py`:

```python
# Google Analytics example
st.markdown('''
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_ID');
</script>
''', unsafe_allow_html=True)
```

### Caching

Implement caching for better performance:

```python
@st.cache_data(ttl=3600)
def get_cached_styles():
    return STYLES
```

## Support

- **Streamlit Issues**: [Streamlit Community](https://discuss.streamlit.io)
- **Napkin AI Issues**: api@napkin.ai
- **App Issues**: [GitHub Issues](https://github.com/yourusername/napkin-api-playground/issues)

## Version History

- **v0.2.1** - Fixed authentication issues, improved error handling
- **v0.2.0** - Initial Streamlit web interface
- **v0.1.x** - CLI only versions

---

Last updated: 2025-08-07