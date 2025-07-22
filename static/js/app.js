// Whisper Audio Transcriber Web App JavaScript

let currentTaskId = null;
let statusCheckInterval = null;

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const uploadBtn = document.getElementById('uploadBtn');
    const progressCard = document.getElementById('progressCard');
    const resultsCard = document.getElementById('resultsCard');
    const errorAlert = document.getElementById('errorAlert');
    const copyBtn = document.getElementById('copyBtn');
    const downloadBtn = document.getElementById('downloadBtn');

    // Handle form submission
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        startTranscription();
    });

    // Copy text functionality
    copyBtn.addEventListener('click', function() {
        const transcriptionText = document.getElementById('transcriptionText');
        transcriptionText.select();
        document.execCommand('copy');
        
        // Show feedback
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '<i class="fas fa-check me-2"></i>Copied!';
        copyBtn.classList.add('btn-success');
        copyBtn.classList.remove('btn-outline-primary');
        
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.classList.remove('btn-success');
            copyBtn.classList.add('btn-outline-primary');
        }, 2000);
    });

    // Download functionality
    downloadBtn.addEventListener('click', function() {
        if (currentTaskId) {
            window.open(`/download/${currentTaskId}`, '_blank');
        }
    });

    function startTranscription() {
        const formData = new FormData(uploadForm);
        const fileName = document.getElementById('audioFile').files[0].name;
        
        // Reset UI
        hideAllCards();
        showProgressCard();
        document.getElementById('fileName').textContent = `File: ${fileName}`;
        
        // Disable upload button
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        
        // Upload file
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
                resetUploadButton();
            } else {
                currentTaskId = data.task_id;
                updateProgress('Transcription started...', 10);
                startStatusChecking();
            }
        })
        .catch(error => {
            showError('Upload failed: ' + error.message);
            resetUploadButton();
        });
    }

    function startStatusChecking() {
        if (statusCheckInterval) {
            clearInterval(statusCheckInterval);
        }
        
        statusCheckInterval = setInterval(() => {
            if (currentTaskId) {
                checkTranscriptionStatus();
            }
        }, 2000);
    }

    function checkTranscriptionStatus() {
        fetch(`/status/${currentTaskId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'processing') {
                updateProgress(data.progress || 'Processing...', 50);
            } else if (data.status === 'completed') {
                clearInterval(statusCheckInterval);
                showResults(data.text);
                resetUploadButton();
            } else if (data.status === 'error') {
                clearInterval(statusCheckInterval);
                showError(data.error || 'Transcription failed');
                resetUploadButton();
            }
        })
        .catch(error => {
            console.error('Status check failed:', error);
        });
    }

    function updateProgress(message, percentage) {
        document.getElementById('progressText').textContent = message;
        const progressBar = document.querySelector('.progress-bar');
        progressBar.style.width = percentage + '%';
        progressBar.setAttribute('aria-valuenow', percentage);
    }

    function showResults(transcriptionText) {
        hideAllCards();
        document.getElementById('transcriptionText').value = transcriptionText;
        resultsCard.style.display = 'block';
        
        // Scroll to results
        resultsCard.scrollIntoView({ behavior: 'smooth' });
    }

    function showError(errorMessage) {
        hideAllCards();
        document.getElementById('errorText').textContent = errorMessage;
        errorAlert.style.display = 'block';
        
        // Scroll to error
        errorAlert.scrollIntoView({ behavior: 'smooth' });
    }

    function showProgressCard() {
        progressCard.style.display = 'block';
        updateProgress('Preparing transcription...', 0);
        
        // Scroll to progress
        progressCard.scrollIntoView({ behavior: 'smooth' });
    }

    function hideAllCards() {
        progressCard.style.display = 'none';
        resultsCard.style.display = 'none';
        errorAlert.style.display = 'none';
    }

    function resetUploadButton() {
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<i class="fas fa-play me-2"></i>Start Transcription';
    }

    // File size validation
    document.getElementById('audioFile').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const maxSize = 100 * 1024 * 1024; // 100MB
            if (file.size > maxSize) {
                showError('File size exceeds 100MB limit. Please choose a smaller file.');
                e.target.value = '';
            }
        }
    });

    // Disable GPU option if not available
    const deviceSelect = document.getElementById('device');
    const gpuOption = deviceSelect.querySelector('option[value="cuda"]');
    if (gpuOption && gpuOption.textContent.includes('Not Available')) {
        gpuOption.disabled = true;
    }
});
