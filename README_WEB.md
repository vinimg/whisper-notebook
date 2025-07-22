# Whisper Audio Transcriber - Web Version

A free online audio transcription service powered by OpenAI Whisper. Convert your audio files to text directly in your browser!

## Features

- 🎵 **Multiple Audio Formats**: Supports MP3, WAV, M4A, MP4, AVI, MOV, MKV
- 🚀 **Multiple Model Sizes**: Choose from Tiny (fastest) to Large (best quality)
- ⚡ **GPU Acceleration**: Automatic CUDA detection for faster processing
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- 🆓 **Completely Free**: No registration or payment required
- 🔒 **Privacy Focused**: Files are processed locally and automatically cleaned up

## Quick Start

### Local Development

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Open Browser**:
   Navigate to `http://localhost:5000`

### Production Deployment

For production deployment with Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: Minimum 4GB (8GB+ recommended for larger models)
- **Storage**: 2GB+ free space for models
- **GPU** (Optional): NVIDIA GPU with CUDA for faster processing

## Model Information

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| Tiny  | ~39MB | Fastest | Basic | Quick transcription, real-time |
| Base  | ~74MB | Fast | Good | Balanced performance |
| Small | ~244MB | Medium | Better | Higher accuracy needed |
| Medium| ~769MB | Slow | Great | Professional use |
| Large | ~1550MB | Slowest | Best | Maximum accuracy |

## API Endpoints

- `GET /` - Main web interface
- `POST /upload` - Upload audio file for transcription
- `GET /status/<task_id>` - Check transcription status
- `GET /download/<task_id>` - Download transcription result
- `GET /health` - Health check endpoint

## Configuration

The application can be configured through environment variables:

- `FLASK_ENV`: Set to `production` for production deployment
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 100MB)
- `UPLOAD_FOLDER`: Directory for uploaded files (default: uploads)
- `OUTPUT_FOLDER`: Directory for transcription results (default: outputs)

## Deployment Options

### 1. Local Server
Perfect for personal use or small teams.

### 2. Cloud Platforms
- **Heroku**: Easy deployment with git
- **DigitalOcean**: VPS with more control
- **AWS EC2**: Scalable cloud deployment
- **Google Cloud**: GPU instances available

### 3. Docker (Coming Soon)
Containerized deployment for easy scaling.

## Troubleshooting

### Common Issues

1. **CUDA Not Available**: 
   - Install NVIDIA drivers and CUDA toolkit
   - Fallback to CPU processing (slower but works)

2. **Out of Memory**:
   - Use smaller model (tiny/base)
   - Reduce file size
   - Add more RAM

3. **File Upload Fails**:
   - Check file size (max 100MB)
   - Verify file format is supported
   - Check available disk space

## Contributing

This is a free, open-source project. Contributions are welcome!

## License

MIT License - Feel free to use, modify, and distribute.

## Support

For issues and questions, please check the troubleshooting section above.

---

**Made with ❤️ using OpenAI Whisper**
