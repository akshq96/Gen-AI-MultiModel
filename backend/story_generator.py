from gemini_client import GeminiClient

STORY_PROMPT = """
You are a highly creative storyteller and creative director. 
Your goal is to write a captivating story segment based on the user's prompt. 
Keep it engaging, visual, and descriptive, around 2-3 paragraphs.
"""

class StoryGenerator:
    def __init__(self, model_name="gemini-1.5-flash"):
        self.client = GeminiClient(model_name=model_name, system_instruction=STORY_PROMPT)

    def generate(self, user_prompt: str, image_reference: str = None) -> str:
        augmented_prompt = user_prompt
        if image_reference:
            augmented_prompt += f"\n\n[Reference Image Data Provided: {image_reference}]"
            
        return self.client.generate_content(augmented_prompt)
