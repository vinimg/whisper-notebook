# 🆓 FREE Deployment Guide for Whisper Web Transcriber

## ⚠️ Important Note About GPU
**Free hosting platforms do NOT support GPU acceleration.** Your transcription will run on CPU, which is slower but still functional. For GPU acceleration, you would need paid hosting.

## 🚀 Best Free Hosting Options

### 1. **Render.com** (Recommended)
- ✅ **Free tier**: 750 hours/month
- ✅ **Easy deployment** from GitHub
- ✅ **Automatic HTTPS**
- ✅ **Good for Whisper apps**

**Steps:**
1. Push your code to GitHub
2. Connect to Render.com
3. Select "Web Service"
4. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --timeout 300 --workers 1 --bind 0.0.0.0:$PORT app_free:app`

### 2. **Railway.app**
- ✅ **$5 free credit monthly**
- ✅ **Very easy deployment**
- ✅ **Good performance**

**Steps:**
1. Connect GitHub repo
2. Deploy automatically
3. Uses `Procfile` configuration

### 3. **Heroku** (Limited Free Tier)
- ⚠️ **Free tier discontinued** but still has some free options
- ✅ **Most documentation available**

**Steps:**
```bash
# Install Heroku CLI
heroku create your-transcriber-name
git add .
git commit -m "Deploy transcriber"
git push heroku main
```

### 4. **Fly.io**
- ✅ **Free allowance** for small apps
- ✅ **Good performance**
- ✅ **Docker-based**

## 📋 Pre-Deployment Checklist

### Files you need:
- ✅ `app_free.py` (CPU-optimized version)
- ✅ `Procfile` (for process management)
- ✅ `requirements.txt` (dependencies)
- ✅ `runtime.txt` (Python version)
- ✅ `templates/` folder (HTML templates)
- ✅ `static/` folder (CSS/JS files)

### Optimizations for free hosting:
- ✅ **CPU-only processing** (no GPU)
- ✅ **Smaller file limit** (25MB instead of 100MB)
- ✅ **Limited models** (tiny, base, small only)
- ✅ **Automatic file cleanup** (saves disk space)
- ✅ **Single worker** (memory efficient)

## 🔧 Quick Setup Commands

```bash
# 1. Prepare for deployment
git init
git add .
git commit -m "Initial commit"

# 2. Push to GitHub
git remote add origin https://github.com/yourusername/whisper-transcriber
git push -u origin main

# 3. Deploy to Render/Railway (connect via web interface)
```

## ⚡ Performance Expectations (CPU-only)

| Model | File Size | Expected Time |
|-------|-----------|---------------|
| Tiny  | 1 minute audio | ~30 seconds |
| Base  | 1 minute audio | ~1 minute |
| Small | 1 minute audio | ~2 minutes |

## 🎯 Recommended Settings for Free Hosting

- **Default Model**: Tiny (fastest)
- **Max File Size**: 25MB
- **Timeout**: 5 minutes
- **Language**: Portuguese (as configured)

## 🔍 Troubleshooting

### Common Issues:
1. **Timeout errors**: Use smaller files or tiny model
2. **Memory errors**: Restart the service
3. **Slow processing**: Expected on CPU - be patient!

### Tips:
- **Test locally first** with `python app_free.py`
- **Use tiny model** for fastest results
- **Keep files under 10MB** for best performance
- **Be patient** - CPU processing takes time

## 💡 Cost-Free Alternatives

If free hosting doesn't work well:

1. **Run locally** and share via ngrok:
   ```bash
   pip install pyngrok
   python app.py
   # In another terminal:
   ngrok http 5000
   ```

2. **Use your own computer** as a server (port forwarding)

3. **Ask friends** to host on their servers

## 🌟 Success Tips

- **Start with tiny model** for testing
- **Use short audio files** initially
- **Monitor usage** to stay within free limits
- **Consider upgrading** to paid hosting if popular

---

**Remember**: Free hosting means CPU-only processing. It will work, but be slower than your local GPU setup!
