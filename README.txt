# Audio Transcriber - Standalone Windows Application

## Quick Start
1. Simply run `AudioTranscriber.exe` to start the application
2. No Python installation required!

## System Requirements
- Windows 10/11 (64-bit)
- 4GB+ RAM recommended
- For GPU support: NVIDIA GPU with CUDA support
- **NO Python installation required** - everything is bundled!

## GPU Support (Optional)
For faster transcription with NVIDIA GPUs:

### Automatic Setup (Recommended)
1. Run the application
2. Click "Install Guide" button
3. Follow the GPU setup instructions

### Manual Setup
1. Install NVIDIA drivers: https://www.nvidia.com/drivers/
2. Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads
3. Run: `pip install torch --index-url https://download.pytorch.org/whl/cu121`

## Features
- Transcribe audio/video files to text
- Support for multiple Whisper models (tiny, base, small, medium, large)
- CPU and GPU processing
- Portuguese language optimization
- Real-time progress tracking

## Supported Formats
- Audio: MP3, WAV, FLAC, M4A
- Video: MP4, MKV, AVI, MOV

## Troubleshooting
- If the app doesn't start, ensure you're running on Windows 10/11 64-bit
- For GPU issues, ensure NVIDIA drivers and CUDA are properly installed
- Check the log console in the app for detailed error messages
- The app may take a few seconds to start (it's extracting bundled files)

## Contact
For support and updates, visit: [Your GitHub/Website]
