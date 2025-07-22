#!/usr/bin/env python3
"""
Windows Packaging Script for Audio Transcriber
Packages the transcriber app into a standalone Windows executable
"""

import os
import sys
import subprocess
import shutil

def create_spec_file():
    """Create a custom PyInstaller spec file for better control"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['transcriber.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'whisper',
        'torch',
        'torchaudio',
        'PyQt5',
        'numpy',
        'scipy',
        'numba',
        'librosa',
        'soundfile',
        'ffmpeg-python'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AudioTranscriber',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)
'''
    
    with open('transcriber.spec', 'w') as f:
        f.write(spec_content)
    print("✓ Created transcriber.spec file")

def install_dependencies():
    """Install packaging dependencies"""
    print("Installing PyInstaller...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    print("✓ PyInstaller installed")

def package_app():
    """Package the application"""
    print("Packaging application...")
    
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # Build using spec file for better control
    subprocess.run([sys.executable, '-m', 'PyInstaller', 'transcriber.spec'], check=True)
    
    print("✓ Application packaged successfully!")
    print("✓ Executable created: dist/AudioTranscriber.exe")

def create_installer_script():
    """Create a simple launcher script (no Python required)"""
    launcher_content = '''@echo off
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
'''
    
    with open('launch_transcriber.bat', 'w') as f:
        f.write(launcher_content)
    print("✓ Created launch_transcriber.bat (optional launcher)")

def create_readme():
    """Create a README for distribution"""
    readme_content = '''# Audio Transcriber - Standalone Windows Application

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
'''
    
    with open('README.txt', 'w') as f:
        f.write(readme_content)
    print("✓ Created README.txt")

def main():
    """Main packaging function"""
    print("Audio Transcriber - Windows Packaging")
    print("====================================")
    print()
    
    try:
        install_dependencies()
        create_spec_file()
        create_installer_script()
        create_readme()
        package_app()
        
        print()
        print("🎉 Packaging complete!")
        print()
        print("Distribution files created:")
        print("- dist/AudioTranscriber.exe (standalone executable - NO Python required!)")
        print("- launch_transcriber.bat (optional launcher)")
        print("- README.txt (user instructions)")
        print()
        print("To distribute:")
        print("1. Copy AudioTranscriber.exe to any Windows machine")
        print("2. Double-click to run - no installation needed!")
        print("3. Optional: Include README.txt and launch_transcriber.bat for users")
        print()
        print("✅ The .exe is completely standalone - no Python required on target machine!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during packaging: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
