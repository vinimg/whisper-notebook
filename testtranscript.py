import whisper
import os

filename = "input.mp3"
model_name = "medium"  # Define your model name here

# Load the model
model = whisper.load_model(model_name)

# Transcribe the audio file
result = model.transcribe(filename, language="pt", word_timestamps=False)

# Print the transcribed text to the terminal
print("Transcribed Text:")
print(result["text"])

# Save the result to a file
output_dir = f"output-{model_name}"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "transcription.txt")

with open(output_path, "w", encoding="utf-8") as f:
    f.write(result["text"])

print(f"Transcription saved to {output_path}")