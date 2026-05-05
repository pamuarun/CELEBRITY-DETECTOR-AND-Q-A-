import os
import io
from PIL import Image
from google import genai

class CelebrityDetector:

    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = "models/gemini-2.5-flash"  # ✅ free-tier multimodal

    def identify(self, image_bytes):
        if not image_bytes:
            return "No face detected", "Unknown"

        prompt = """
Identify the celebrity in this image.

Return strictly in this format:
Full Name: <name>
Profession: <profession>
Nationality: <nationality>
Famous For: <reason>
Top Achievements:
- <achievement 1>
- <achievement 2>

If you cannot identify the person, return exactly 'Unknown'.
"""

        try:
            print("DEBUG: Sending request to Gemini...")

            # ✅ Convert bytes → PIL Image
            image = Image.open(io.BytesIO(image_bytes))

            # ✅ CLEAN & CORRECT MULTIMODAL CALL
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt, image]
            )

            print("DEBUG RAW RESPONSE:")
            print(response)

            # ✅ Safely extract text
            result = getattr(response, "text", "")

            print("DEBUG PARSED RESPONSE:")
            print(result)

            if not result:
                return "Error detecting celebrity", "Unknown"

            if "Unknown" in result:
                return "Unknown", "Unknown"

            name = self.extract_name(result)

            print(f"DEBUG: Extracted Name → {name}")

            return result, name

        except Exception as e:
            print(f"ERROR: {str(e)}")
            return "Error detecting celebrity", "Unknown"

    def extract_name(self, content):
        if not content:
            return "Unknown"

        for line in content.splitlines():
            if "full name" in line.lower():
                return line.split(":")[-1].strip()

        return "Unknown"