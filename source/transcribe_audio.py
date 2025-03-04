import whisper

FILE_MP3_NAME = "./temp/recorded_audio.mp3"

model = whisper.load_model("tiny")

result = model.transcribe(FILE_MP3_NAME)

print("Transcription:")
print(result["text"])