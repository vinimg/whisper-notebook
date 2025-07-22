@echo off
echo Audio Transcriber - Standalone Version
echo ======================================
echo.
echo Starting Audio Transcriber...
echo.

REM Check if the executable exists
if not exist "AudioTranscriber.exe" (
    echo ERROR: AudioTranscriber.exe not found!
    echo Please ensure AudioTranscriber.exe is in the same folder as this script.
    pause
    exit /b 1
)

REM Launch the application
start "" "AudioTranscriber.exe"

echo Audio Transcriber started successfully!
echo.
echo Note: For GPU acceleration, you may need:
echo 1. NVIDIA drivers from https://www.nvidia.com/drivers/
echo 2. CUDA Toolkit from https://developer.nvidia.com/cuda-downloads
echo.
echo The application will work with CPU-only mode by default.
pause
