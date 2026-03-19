from gemini_client import GeminiClient

NARRATOR_PROMPT = """
You are a professional voiceover scriptwriter and audio director.
Based on the provided story segment, create a narration script optimized for a 
Voice Actor or Text-to-Speech (TTS) engine.
Add light pacing or emotional director notes in [brackets].
Do not include any other conversational filler.
"""

class NarrationGenerator:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.client = GeminiClient(model_name=model_name, system_instruction=NARRATOR_PROMPT)

    def generate(self, story_text: str) -> str:
        prompt = f"Create a voiceover narration script for this story segment:\n\n{story_text}"
        return self.client.generate_content(prompt)
