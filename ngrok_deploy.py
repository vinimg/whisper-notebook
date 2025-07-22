#!/usr/bin/env python3
"""
Instant free deployment using ngrok - keeps your GPU power!
Run this to make your transcriber accessible online for free.
"""

import subprocess
import sys
import time
from pyngrok import ngrok
import threading

def start_flask_app():
    """Start the Flask app in a separate thread"""
    subprocess.run([sys.executable, "app.py"])

def main():
    print("🚀 Starting Whisper Transcriber with ngrok...")
    print("This will make your GPU-powered transcriber accessible online for FREE!")
    print()
    
    # Start Flask app in background
    flask_thread = threading.Thread(target=start_flask_app, daemon=True)
    flask_thread.start()
    
    # Wait for Flask to start
    print("⏳ Starting Flask server...")
    time.sleep(5)
    
    # Create ngrok tunnel
    print("🌐 Creating public tunnel...")
    try:
        # Create tunnel to Flask app
        public_url = ngrok.connect(5000)
        
        print("✅ SUCCESS! Your transcriber is now online!")
        print(f"🔗 Public URL: {public_url}")
        print()
        print("📋 Share this URL with anyone to use your transcriber!")
        print("💡 Features:")
        print("   - GPU acceleration (your hardware)")
        print("   - All model sizes available")
        print("   - 100MB file limit")
        print("   - Fast processing")
        print()
        print("⚠️  Keep this terminal open to maintain the connection")
        print("🛑 Press Ctrl+C to stop the service")
        print()
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping service...")
            ngrok.disconnect(public_url)
            print("✅ Service stopped")
            
    except Exception as e:
        print(f"❌ Error creating tunnel: {e}")
        print("💡 You may need to sign up for a free ngrok account at https://ngrok.com")

if __name__ == "__main__":
    main()
