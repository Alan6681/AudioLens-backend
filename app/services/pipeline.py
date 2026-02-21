import os
import re
from dotenv import load_dotenv
from app.services.transcription import TranscriptionService
from app.services.summarization import SummarizationService
from app.services.sources import ResourceService

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
youtube_api_key = os.getenv("YOUTUBE_API_KEY")


class AudioLensPipeline:
    def __init__(self):
        self.transcription_service = TranscriptionService(api_key=api_key)
        self.summarization_service = SummarizationService(api_key=api_key)
        self.resource_service = ResourceService(youtube_api_key=youtube_api_key)

    def extract_topics(self, summary: str) -> list[str]:
        """
        Parses the ## 🔍 Suggested Topics to Explore Further section
        from the summary output and returns a list of topic strings.
        """
        topics = []

        # Find the suggested topics section
        match = re.search(
            r"##\s*🔍\s*Suggested Topics to Explore Further(.*?)(?=##|$)",
            summary,
            re.DOTALL
        )

        if not match:
            print("⚠️ Could not find suggested topics section in summary")
            return topics

        section = match.group(1).strip()

        # Extract each bullet point line
        for line in section.splitlines():
            line = line.strip()
            # Remove bullet markers like -, *, 1., 2. etc
            line = re.sub(r"^[-*•]\s*|\d+\.\s*", "", line).strip()
            # Remove any bold markdown like **topic**
            line = re.sub(r"\*\*(.*?)\*\*", r"\1", line).strip()
            if ":" in line:
                line = line.split(":")[0].strip()
            if line and not line.endswith(":"):  
                topics.append(line)

        return topics[:5] 

    def run(self, audio_file_path: str) -> dict:
        print("\n🎙️ Step 1: Transcribing audio...")
        transcript = self.transcription_service.transcribe(audio_file_path)
        print(f"✅ Transcription complete — {len(transcript.split())} words\n")

        print("🧠 Step 2: Summarizing transcript...")
        summary = self.summarization_service.summarize(transcript)
        print("✅ Summary complete\n")

        print("🔍 Step 3: Extracting topics...")
        topics = self.extract_topics(summary)
        print(f"✅ Found {len(topics)} topics: {topics}\n")

        print("📺 Step 4: Fetching YouTube resources...")
        resources = self.resource_service.fetch_resources(topics)
        print("✅ Resources fetched\n")

        return {
            "transcript": transcript,
            "summary": summary,
            "topics": topics,
            "resources": resources,
        }


if __name__ == "__main__":
    pipeline = AudioLensPipeline()
    result = pipeline.run("Physics lecture.m4a")

    print("\n" + "="*60)
    print("📚 SUMMARY")
    print("="*60)
    print(result["summary"])

    print("\n" + "="*60)
    print("📺 RESOURCES")
    print("="*60)
    for topic, videos in result["resources"].items():
        print(f"\n🔹 {topic}")
        for video in videos:
            print(f"   - {video['title']} by {video['channel']}")
            print(f"     {video['url']}")
