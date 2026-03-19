from gemini_client import GeminiClient

IMAGE_PROMPT = """
You are an expert art director and prompt engineer.
Based on the provided story segment, create a singular highly detailed, descriptive prompt 
that could be given to an AI image generator (like Imagen 3, Midjourney, or DALL-E) 
to create an illustration capturing the essence of the story.
Be specific about style, lighting, composition, and subjects.
Return ONLY the prompt string, with no introductory text.
"""

class ImagePromptGenerator:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.client = GeminiClient(model_name=model_name, system_instruction=IMAGE_PROMPT)

    def generate(self, story_text: str) -> str:
        prompt = f"Create an illustration prompt based on this story:\n\n{story_text}"
        return self.client.generate_content(prompt)
