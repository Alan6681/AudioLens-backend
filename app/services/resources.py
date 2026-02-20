import os
from dotenv import load_dotenv
import requests

load_dotenv()

class ResourceService:
    def __init__(self, youtube_api_key:str):
        if not youtube_api_key:
            raise ValueError("API key is required for resource service.")
        self.youtube_api_key = youtube_api_key
        self.base_url = "https://www.googleapis.com/youtube/v3/search"

    def fetch_resources(self, topics: list[str], max_results: int = 3) -> dict:
        results = {}

        for topic in topics:
            print(f"Fetching YouTube videos for: {topic}")
            try:
                params = {
                    "part": "snippet",
                    "q": topic,
                    "type": "video",
                    "maxResults": max_results,
                    "relevanceLanguage": "en",
                    "key": self.youtube_api_key,
                }

                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                items = response.json().get("items", [])

                results[topic] = [
                    {
                        "type": "youtube",
                        "title": item["snippet"]["title"],
                        "channel": item["snippet"]["channelTitle"],
                        "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                        "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                    }
                    for item in items[:3]
                ]

            except Exception as e:
                print(f"Failed to fetch videos for '{topic}': {e}")
                results[topic] = []

        return results
    
if __name__ == "__main__":
    service = ResourceService(youtube_api_key=os.getenv("YOUTUBE_API_KEY"))

    topics = [
        "Newton's Second Law of Motion",
        "Kinetic and Potential Energy",
    ]

    resources = service.fetch_resources(topics)

    for topic, videos in resources.items():
        print(f"\n=== {topic} ===")
        for video in videos:
            print(f"  - {video['title']} by {video['channel']}")
            print(f"    {video['url']}")




    