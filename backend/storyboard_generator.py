from gemini_client import GeminiClient

STORYBOARD_PROMPT = """
You are an expert film and animation director.
Provide a concise, vivid storyboard prompt (1-2 sentences) describing how the camera 
should move and what it focuses on during the given story scene. 
This prompt will be fed into a Text-to-Video AI model (like Google Veo, Sora or Runway).
Return ONLY the camera/action prompt format.
"""

class StoryboardGenerator:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.client = GeminiClient(model_name=model_name, system_instruction=STORYBOARD_PROMPT)

    def generate(self, story_text: str) -> str:
        prompt = f"Create a short video storyboard prompt for this scene:\n\n{story_text}"
        return self.client.generate_content(prompt)
