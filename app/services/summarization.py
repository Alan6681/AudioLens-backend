from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os
from transcription import TranscriptionService

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

SUMMARIZATION_PROMPT = """
You are an expert academic assistant specialized in analyzing and summarizing lecture transcripts.

You will be given a raw lecture transcript that may contain filler words, repetitions, and informal speech.
Your job is to transform it into a clean, detailed, and well-structured set of lecture notes.

Return your response in the following structure:

---

## 📚 Lecture Title
Infer a suitable title from the content of the lecture.

## 🎯 Overview
A 3-5 sentence paragraph summarizing the entire lecture at a high level. 
What was the lecture about? What was the lecturer trying to teach?

## 🧠 Key Concepts
List and explain every major concept introduced in the lecture.
For each concept provide:
- **Concept name**
- A clear 2-4 sentence explanation in simple terms
- Any examples the lecturer used to explain it

## 📝 Detailed Notes
A thorough section-by-section breakdown of the lecture following the order it was taught.
Write this as proper notes a student would use to study from.
Be detailed — do not leave out important points.

## 💡 Important Definitions
Extract every definition, formula, or rule mentioned in the lecture and list them clearly.

## ⚠️ Key Takeaways
3-7 bullet points of the most important things the student must remember from this lecture.

## ❓ Possible Exam Questions
Generate 5 likely exam or quiz questions based on the content of this lecture.

## 🔍 Suggested Topics to Explore Further
List 3-5 specific topics or concepts from this lecture that the student should research further to deepen their understanding.
These will be used to fetch external resources so be specific (e.g. "Newton's Second Law of Motion" not just "physics").

---

Important rules:
- Write clearly and at a level appropriate for a university student
- Do not make up information that was not in the transcript
- If the transcript is unclear or incomplete in places, note it honestly
- Keep the Suggested Topics as specific and searchable as possible
"""

class SummarizationService:
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        if not api_key:
            raise ValueError("API key is required for summarization service.")
        self.model = model
        self.client = ChatGroq(api_key=api_key, model=self.model)

    def summarize(self, text: str) -> str:
        if not text or not text.strip():
            raise ValueError("Transcript is empty")
            
        response = self.client.invoke([
            SystemMessage(content=SUMMARIZATION_PROMPT),
            HumanMessage(content=f"Here is the lecture transcript:\n\n{text}")
        ])

        return response.content


if __name__ == "__main__":
    transcription_service = TranscriptionService(api_key=api_key)
    summarization_service = SummarizationService(api_key=api_key)

    transcript = transcription_service.transcribe("Ceremony.m4a")
    summary = summarization_service.summarize(transcript)
    print(summary)