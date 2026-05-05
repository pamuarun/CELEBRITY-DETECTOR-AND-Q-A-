import os
from google import genai

class QAEngine:

    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = "models/gemini-2.5-flash"

    def ask_about_celebrity(self, name, question):
        prompt = f"""
You are an AI assistant.

Answer the question about {name} in a clean, simple paragraph.

STRICT RULES:
- Do NOT use markdown
- Do NOT use *, **, -, bullet points
- Do NOT format text
- Only plain English sentences
- Keep it short and neat (3-4 lines max)

Question: {question}
"""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )

            text = response.text if response.text else ""

            # ✅ Clean formatting (backup safety)
            clean_text = (
                text.replace("*", "")
                    .replace("#", "")
                    .replace("`", "")
                    .replace("-", "")
            )

            return clean_text.strip()

        except Exception:
            return "Sorry, I couldn't find a clean answer."