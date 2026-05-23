# Deployment Guide

This guide covers deploying the Stock Analysis Dashboard to production.

## Option 1: Streamlit Cloud (Recommended)

The easiest way to deploy this app is using Streamlit Cloud.

### Steps:

1. **Prepare Your Repository**
   - Ensure all files are pushed to GitHub
   - Verify `requirements.txt` is in the root directory

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository: `phfp99wv7v-star/jusik`
   - Set branch to `main`
   - Set main file path to `app.py`
   - Click "Deploy"

3. **Access Your App**
   - Your app will be available at: `https://jusik.streamlit.app` (or similar)
   - Share the URL with others

### Updating Your App:
Just push changes to GitHub - Streamlit Cloud will automatically redeploy!

## Option 2: Docker

### Create Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run:

```bash
# Build image
docker build -t jusik-app .

# Run container
docker run -p 8501:8501 jusik-app
```

## Option 3: Heroku

### Steps:

1. **Create Procfile:**
   ```
   web: streamlit run app.py --logger.level=error
   ```

2. **Create runtime.txt:**
   ```
   python-3.9.16
   ```

3. **Deploy:**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

## Option 4: Self-Hosted (Linux/VPS)

### Steps:

1. **SSH into your server:**
   ```bash
   ssh user@your-server.com
   ```

2. **Clone and setup:**
   ```bash
   git clone https://github.com/phfp99wv7v-star/jusik.git
   cd jusik
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run with supervisor/systemd:**
   
   Create `/etc/systemd/system/jusik.service`:
   ```ini
   [Unit]
   Description=Stock Analysis Dashboard
   After=network.target

   [Service]
   Type=simple
   User=your-user
   WorkingDirectory=/path/to/jusik
   ExecStart=/path/to/jusik/venv/bin/streamlit run app.py --server.port=8501
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Then:
   ```bash
   sudo systemctl enable jusik
   sudo systemctl start jusik
   ```

4. **Setup reverse proxy (nginx):**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
       }
   }
   ```

## Environment Variables

If you need to add secrets (API keys, etc.), create a `.streamlit/secrets.toml` file:

```toml
# Example (don't commit this file!)
api_key = "your-secret-key"
```

Access in app:
```python
import streamlit as st
api_key = st.secrets["api_key"]
```

## Performance Tips

1. **Enable Caching** - Already implemented in `app.py` with `@st.cache_data`
2. **Optimize Data** - Limit historical data to 1-2 years
3. **Use CDN** - For static assets (if any)
4. **Monitor Resources** - Check memory/CPU usage

## Troubleshooting

### App is slow
- Check network connection
- Reduce data period (use 1mo or 3mo instead)
- Clear Streamlit cache: `streamlit cache clear`

### API rate limits
- yfinance has rate limits
- Increase cache TTL in code (currently 3600 seconds = 1 hour)
- Consider upgrade if using Streamlit Cloud

### Deployment failed
- Check `requirements.txt` format
- Verify all imports are available
- Check GitHub Actions logs (if using CI/CD)

## Monitoring

For Streamlit Cloud, monitor your app:
- View logs in Streamlit Cloud dashboard
- Set up email alerts for errors
- Monitor resource usage

---

For more help, visit:
- [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-cloud/deploy-your-app)
- [Docker Documentation](https://docs.docker.com/)
