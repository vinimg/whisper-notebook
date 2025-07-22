import sys
import os
import threading
import subprocess
import re
import platform
import webbrowser
import whisper
import torch
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QFileDialog,
    QComboBox, QRadioButton, QTextEdit, QMessageBox
)
from PyQt5.QtCore import pyqtSignal, QObject

class Worker(QObject):
    log = pyqtSignal(str)
    finished_task = pyqtSignal(str, str)

    def download_model(self, model_name, device):
        message = f"Downloading model '{model_name}' on {device}..."
        self.log.emit(message)
        print(message)
        whisper.load_model(model_name, device=device)
        done = f"Model '{model_name}' downloaded successfully!"
        self.log.emit(done)
        print(done)
        self.finished_task.emit('download', model_name)

    def transcribe(self, filename, model_name, device, output_dir):
        start_msg = "Starting transcription via CLI..."
        self.log.emit(start_msg)
        print(start_msg)

        cmd = [
            sys.executable, "-m", "whisper", filename,
            "--model", model_name,
            "--language", "pt",
            "--device", device,
            "--verbose", "True",
            "--output_dir", output_dir
        ]
        os.makedirs(output_dir, exist_ok=True)

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        for line in process.stdout:
            line = line.rstrip()
            self.log.emit(line)
            print(line)
        process.wait()

        base = os.path.splitext(os.path.basename(filename))[0]
        transcript_path = os.path.join(output_dir, f"{base}.txt")
        if os.path.exists(transcript_path):
            complete_msg = "Transcription complete!"
            self.log.emit(complete_msg)
            print(complete_msg)
            self.finished_task.emit('transcribe', transcript_path)
        else:
            fail_msg = "Transcription failed or output not found."
            self.log.emit(fail_msg)
            print(fail_msg)
            self.finished_task.emit('transcribe', "")

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Whisper Transcriber")
        self.worker = Worker()
        self.init_ui()
        self.connect_signals()
        self.check_gpu_status()

    def init_ui(self):
        layout = QVBoxLayout()

        # File selection
        file_layout = QHBoxLayout()
        self.file_label = QLineEdit()
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(QLabel("Audio/Video File:"))
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)

        # Model & device
        model_layout = QHBoxLayout()
        self.model_cb = QComboBox()
        self.model_cb.addItems(['tiny', 'base', 'small', 'medium', 'large'])
        self.device_cpu = QRadioButton("CPU")
        self.device_cpu.setChecked(True)
        self.device_gpu = QRadioButton("GPU")
        model_layout.addWidget(QLabel("Model:"))
        model_layout.addWidget(self.model_cb)
        model_layout.addWidget(QLabel("Device:"))
        model_layout.addWidget(self.device_cpu)
        model_layout.addWidget(self.device_gpu)
        layout.addLayout(model_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.download_btn = QPushButton("Download Model")
        self.transcribe_btn = QPushButton("Transcribe")
        self.install_btn = QPushButton("Install Guide")
        self.cuda_btn = QPushButton("CUDA Setup")
        btn_layout.addWidget(self.download_btn)
        btn_layout.addWidget(self.transcribe_btn)
        btn_layout.addWidget(self.install_btn)
        btn_layout.addWidget(self.cuda_btn)
        layout.addLayout(btn_layout)

        # Log console
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.setLayout(layout)

    def connect_signals(self):
        self.download_btn.clicked.connect(self.handle_download)
        self.transcribe_btn.clicked.connect(self.handle_transcribe)
        self.install_btn.clicked.connect(self.show_install_guide)
        self.cuda_btn.clicked.connect(self.auto_install_cuda_drivers)
        self.worker.log.connect(self.append_log)
        self.worker.finished_task.connect(self.on_finished)

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Media File", "", "Media Files (*.mp3 *.wav *.mp4 *.mkv)")
        if path:
            self.file_label.setText(path)

    def handle_download(self):
        model = self.model_cb.currentText()
        device = 'cuda' if self.device_gpu.isChecked() else 'cpu'
        threading.Thread(
            target=self.worker.download_model,
            args=(model, device), daemon=True
        ).start()

    def handle_transcribe(self):
        filename = self.file_label.text().strip()
        if not filename or not os.path.exists(filename):
            QMessageBox.critical(self, "Error", "Please select a valid input file.")
            return
        model = self.model_cb.currentText()
        device = 'cuda' if self.device_gpu.isChecked() else 'cpu'
        output_dir = f"output-{model}"
        threading.Thread(
            target=self.worker.transcribe,
            args=(filename, model, device, output_dir), daemon=True
        ).start()

    def show_install_guide(self):
        guide = (
            "**Windows Installation Guide**\n\n"
            "1. Install Python 3.8+ from https://www.python.org/downloads/windows/, check 'Add to PATH'.\n"
            "2. Open PowerShell as Administrator.\n"
            "3. Create & activate a virtual environment:\n"
            "   python -m venv whisper_env\n"
            "   whisper_env\Scripts\Activate\n\n"
            "4. Install dependencies (CPU only):\n"
            "   pip install --upgrade pip\n"
            "   pip install openai-whisper PyQt5 torch --index-url https://download.pytorch.org/whl/cpu\n\n"
            "5. (Optional GPU) After NVIDIA driver & CUDA toolkit install:\n"
            "   pip install --upgrade pip\n"
            "   pip install torch --index-url https://download.pytorch.org/whl/cu121\n\n"
            "6. Run the app:\n"
            "   python whisper_gui.py\n\n"
            "**Packaging**\n"
            "- pip install pyinstaller\n"
            "- pyinstaller --onefile --windowed whisper_gui.py\n"
            "- Distribute the .exe found in 'dist\'."
        )
        QMessageBox.information(self, "Installation Guide", guide)

    def append_log(self, message):
        self.log.append(message)

    def on_finished(self, task, info):
        if task == 'download':
            self.append_log(f"Downloaded model: {info}")
        elif task == 'transcribe':
            if info:
                self.append_log(f"Saved transcription to: {info}")
            else:
                self.append_log("No transcription file found.")

    def check_gpu_status(self):
        """Check GPU availability and update UI accordingly"""
        try:
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                self.append_log(f"✓ GPU detected: {gpu_name}")
                self.device_gpu.setEnabled(True)
            else:
                self.append_log("⚠ No CUDA GPU detected - CPU only mode")
                self.device_gpu.setEnabled(False)
                self.device_cpu.setChecked(True)
        except Exception as e:
            self.append_log(f"⚠ GPU check failed: {e}")
            self.device_gpu.setEnabled(False)

    def detect_nvidia_gpu(self):
        """Detect NVIDIA GPU hardware"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name'], 
                                      capture_output=True, text=True)
                return 'nvidia' in result.stdout.lower()
            else:
                result = subprocess.run(['lspci'], capture_output=True, text=True)
                return 'nvidia' in result.stdout.lower()
        except:
            return False

    def auto_install_cuda_drivers(self):
        """Provide automated CUDA driver installation guidance"""
        if not self.detect_nvidia_gpu():
            QMessageBox.warning(self, "No NVIDIA GPU", 
                              "No NVIDIA GPU detected. GPU acceleration requires an NVIDIA graphics card.")
            return

        msg = QMessageBox()
        msg.setWindowTitle("CUDA Driver Installation")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Automated CUDA setup detected NVIDIA GPU. Choose installation method:")
        
        # Add custom buttons
        auto_btn = msg.addButton("Auto Download", QMessageBox.ActionRole)
        manual_btn = msg.addButton("Manual Instructions", QMessageBox.ActionRole)
        cancel_btn = msg.addButton("Cancel", QMessageBox.RejectRole)
        
        msg.exec_()
        
        if msg.clickedButton() == auto_btn:
            self.download_cuda_drivers()
        elif msg.clickedButton() == manual_btn:
            self.show_manual_cuda_instructions()

    def download_cuda_drivers(self):
        """Automatically download CUDA drivers"""
        try:
            # Open NVIDIA driver download page
            webbrowser.open("https://www.nvidia.com/drivers/")
            
            # Open CUDA toolkit download page
            webbrowser.open("https://developer.nvidia.com/cuda-downloads")
            
            QMessageBox.information(self, "Driver Download", 
                                  "Opened NVIDIA driver and CUDA toolkit download pages in your browser.\n\n"
                                  "Please:\n"
                                  "1. Download and install the latest NVIDIA drivers\n"
                                  "2. Download and install CUDA Toolkit 12.1+\n"
                                  "3. Restart the application after installation")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open download pages: {e}")

    def show_manual_cuda_instructions(self):
        """Show detailed manual CUDA installation instructions"""
        instructions = (
            "**Manual CUDA Installation Guide**\n\n"
            "**Step 1: Install NVIDIA Drivers**\n"
            "1. Visit: https://www.nvidia.com/drivers/\n"
            "2. Select your GPU model and OS\n"
            "3. Download and install the latest driver\n\n"
            "**Step 2: Install CUDA Toolkit**\n"
            "1. Visit: https://developer.nvidia.com/cuda-downloads\n"
            "2. Select Windows > x86_64 > your version\n"
            "3. Download and run the installer\n"
            "4. Choose 'Express Installation'\n\n"
            "**Step 3: Install GPU PyTorch**\n"
            "Open Command Prompt as Administrator and run:\n"
            "pip uninstall torch torchvision torchaudio\n"
            "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121\n\n"
            "**Step 4: Verify Installation**\n"
            "Restart this application and check if GPU option is enabled.\n\n"
            "**Troubleshooting:**\n"
            "- Restart your computer after driver installation\n"
            "- Ensure Windows is up to date\n"
            "- Check Windows Device Manager for GPU recognition"
        )
        QMessageBox.information(self, "CUDA Installation Guide", instructions)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())

# Packaging Instructions:
# 1. pip install pyinstaller
# 2. pyinstaller --onefile --windowed transcriber.py
