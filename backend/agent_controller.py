import json
import asyncio
from story_generator import StoryGenerator
from image_prompt_generator import ImagePromptGenerator
from narration_generator import NarrationGenerator
from storyboard_generator import StoryboardGenerator

class AgentController:
    """
    Orchestrates the generation flow and yields SSE chunks 
    to create the interleaved multimodal effect on the frontend.
    """
    def __init__(self):
        self.story_gen = StoryGenerator()
        self.image_gen = ImagePromptGenerator()
        self.narrator = NarrationGenerator()
        self.storyboard_gen = StoryboardGenerator()

    async def stream_experience(self, user_prompt: str, image_reference: str = None):
        """
        Yields JSON payloads sequentially formatted for SSE.
        """
        # Step 1: Initial Acknowledgement
        yield self._format_chunk("status", "Initializing Creative Studio AI...")
        await asyncio.sleep(0.5)

        # Step 2: Story Generation
        yield self._format_chunk("status", "Drafting story narrative...")
        story = self.story_gen.generate(user_prompt, image_reference)
        yield self._format_chunk("story", story)
        await asyncio.sleep(0.5)

        # Step 3: Scene Illustration Prompt
        yield self._format_chunk("status", "Visualizing key scene...")
        image_prompt = self.image_gen.generate(story)
        yield self._format_chunk("image_prompt", image_prompt)
        # Here you would theoretically call your Imagen 3 / Vertex AI Image generator 
        # and upload via self.media_storage to get a REAL URL back.
        await asyncio.sleep(0.5)

        # Step 4: Narration Script
        yield self._format_chunk("status", "Writing voiceover script...")
        narration = self.narrator.generate(story)
        yield self._format_chunk("narration", narration)
        await asyncio.sleep(0.5)

        # Step 5: Storyboard Generation
        yield self._format_chunk("status", "Directing animation storyboard...")
        storyboard = self.storyboard_gen.generate(story)
        yield self._format_chunk("storyboard", storyboard)
        await asyncio.sleep(0.5)

        # Step 6: Completion
        yield self._format_chunk("status", "Experience completed.")
        yield self._format_chunk("done", True)
        
def _format_chunk(self, action_type: str, data):
    return {
        "event": action_type,
        "data": json.dumps({"type": action_type, "data": data})
    }