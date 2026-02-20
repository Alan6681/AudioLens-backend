from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# with open("Ceremony.m4a", "rb") as audio_file:
#     transcription = client.audio.transcriptions.create(
#         file=audio_file,
#         model="whisper-large-v3-turbo",
#     )

# print(transcription.text)

class TranscriptionService:
    SURPORTED_AUDIO_FORMATS = ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]

    def __init__(self, api_key:str, model:str = "whisper-large-v3-turbo",):
        if not api_key:
            raise ValueError("API key is required for transcription service.")
        self.client = Groq(api_key=api_key)
        self.model = model

    def _validate_file(self, audio_file_path:str):
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

        if not any(audio_file_path.endswith(ext) for ext in self.SURPORTED_AUDIO_FORMATS):
            raise ValueError(f"Unsupported audio format. Supported formats: {', '.join(self.SURPORTED_AUDIO_FORMATS)}")


    def transcribe(self, audio_file_path:str) -> str:
        self._validate_file(audio_file_path)

        with open(audio_file_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                file=audio_file,
                model=self.model,
            )
        
        return transcription.text
    

# if __name__ == "__main__":
#     api_key = os.getenv("GROQ_API_KEY")
#     service = TranscriptionService(api_key=api_key)
#     result = service.transcribe("Ceremony.m4a")

#     print(result)