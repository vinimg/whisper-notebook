import os
import threading
import subprocess
import sys
import uuid
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import whisper
import torch

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024  # 25MB max for free hosting
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Global variables to track transcription status
transcription_status = {}
# Limit models for free hosting (smaller models only)
available_models = ["tiny", "base", "small"]

def check_gpu_status():
    """Always return CPU for free hosting"""
    return "cpu"

def transcribe_audio(task_id, filename, model_name, device, output_dir):
    """Transcribe audio file using Whisper CLI - optimized for free hosting"""
    try:
        transcription_status[task_id] = {"status": "processing", "progress": "Starting transcription..."}
        
        # Force CPU and optimize for free hosting
        cmd = [
            sys.executable, "-m", "whisper", filename,
            "--model", model_name,
            "--language", "pt",
            "--device", "cpu",  # Force CPU
            "--output_dir", output_dir
        ]
        
        transcription_status[task_id]["progress"] = "Running Whisper transcription on CPU..."
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        output_lines = []
        for line in iter(process.stdout.readline, ''):
            if line:
                output_lines.append(line.strip())
                transcription_status[task_id]["progress"] = line.strip()
        
        process.wait()
        
        if process.returncode == 0:
            # Find the generated text file
            base_name = os.path.splitext(os.path.basename(filename))[0]
            txt_file = os.path.join(output_dir, f"{base_name}.txt")
            
            if os.path.exists(txt_file):
                with open(txt_file, 'r', encoding='utf-8') as f:
                    transcription_text = f.read()
                
                transcription_status[task_id] = {
                    "status": "completed",
                    "text": transcription_text,
                    "txt_file": txt_file
                }
                
                # Clean up uploaded file to save space
                if os.path.exists(filename):
                    os.remove(filename)
                    
            else:
                transcription_status[task_id] = {
                    "status": "error",
                    "error": "Transcription file not found"
                }
        else:
            transcription_status[task_id] = {
                "status": "error",
                "error": f"Transcription failed with return code {process.returncode}"
            }
            
    except Exception as e:
        transcription_status[task_id] = {
            "status": "error",
            "error": str(e)
        }
    finally:
        # Clean up uploaded file in case of error
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass

@app.route('/')
def index():
    """Main page"""
    device = check_gpu_status()
    return render_template('index.html', device=device, models=available_models)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and start transcription"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    model = request.form.get('model', 'tiny')  # Default to tiny for speed
    device = "cpu"  # Force CPU for free hosting
    
    # Ensure model is in allowed list
    if model not in available_models:
        model = "tiny"
    
    if file:
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{task_id}_{filename}")
        file.save(filepath)
        
        # Create output directory for this task
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], task_id)
        os.makedirs(output_dir, exist_ok=True)
        
        # Start transcription in background thread
        thread = threading.Thread(
            target=transcribe_audio,
            args=(task_id, filepath, model, device, output_dir)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'task_id': task_id,
            'message': 'Transcription started (CPU processing)',
            'filename': filename
        })

@app.route('/status/<task_id>')
def get_status(task_id):
    """Get transcription status"""
    if task_id in transcription_status:
        return jsonify(transcription_status[task_id])
    else:
        return jsonify({'status': 'not_found'}), 404

@app.route('/download/<task_id>')
def download_result(task_id):
    """Download transcription result"""
    if task_id in transcription_status:
        status = transcription_status[task_id]
        if status.get('status') == 'completed' and 'txt_file' in status:
            return send_file(status['txt_file'], as_attachment=True)
    
    return jsonify({'error': 'File not found'}), 404

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
