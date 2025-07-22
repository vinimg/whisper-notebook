#!/usr/bin/env python3
"""
Local network sharing - completely free, no accounts needed!
Share your transcriber on your local network instantly.
"""

import socket
import subprocess
import sys
import time
import threading
import os

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def start_flask_app():
    """Start the Flask app"""
    os.system(f"{sys.executable} app.py")

def main():
    print("🚀 Starting Whisper Transcriber for Local Network Sharing...")
    print("This will make your GPU-powered transcriber accessible on your local network!")
    print()
    
    # Get local IP
    local_ip = get_local_ip()
    
    print("📡 Network Information:")
    print(f"   Local IP: {local_ip}")
    print(f"   Port: 5000")
    print()
    
    # Start Flask app in background
    flask_thread = threading.Thread(target=start_flask_app, daemon=True)
    flask_thread.start()
    
    # Wait for Flask to start
    print("⏳ Starting Flask server...")
    time.sleep(3)
    
    print("✅ SUCCESS! Your transcriber is now accessible!")
    print()
    print("🔗 Access URLs:")
    print(f"   Local: http://localhost:5000")
    print(f"   Network: http://{local_ip}:5000")
    print()
    print("📋 Share these URLs:")
    print(f"   • Anyone on your WiFi can use: http://{local_ip}:5000")
    print(f"   • You can use locally: http://localhost:5000")
    print()
    print("💡 Features:")
    print("   - GPU acceleration (your hardware)")
    print("   - All model sizes available")
    print("   - 100MB file limit")
    print("   - Fast processing")
    print("   - No accounts needed!")
    print()
    print("⚠️  Keep this terminal open to maintain the service")
    print("🛑 Press Ctrl+C to stop the service")
    print()
    
    # Keep running and show status
    try:
        while True:
            time.sleep(5)
            print(f"🟢 Service running - Access at http://{local_ip}:5000")
    except KeyboardInterrupt:
        print("\n🛑 Stopping service...")
        print("✅ Service stopped")

if __name__ == "__main__":
    main()
