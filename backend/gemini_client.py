# import google.generativeai as genai
# import os
# from typing import Optional, List
# from dotenv import load_dotenv

# class GeminiClient:
#     def __init__(self, model_name: str = "gemini-2.5-flash", system_instruction: str = None):
#         """
#         Initializes the Gemini model using the GenAI SDK. 
#         Requires GEMINI_API_KEY in the environment.
#         """
#         # Force reload environment variables to catch live changes to .env
#         load_dotenv(override=True)
        
#         api_key = os.getenv("GEMINI_API_KEY")
#         if not api_key:
#             print("WARNING: GEMINI_API_KEY is not set.")
#         else:
#             genai.configure(api_key=api_key)

#         self.model = genai.GenerativeModel(
#             model_name=model_name,
#             system_instruction=system_instruction
#         )

#     def generate_content(self, user_prompt: str) -> str:
#         """
#         Generates standard text content from a prompt.
#         """
#         try:
#             response = self.model.generate_content(user_prompt)
#             if response and hasattr(response, 'text'):
#                 return response.text
#             return ""
#         except Exception as e:
#             print(f"Error generating content: {e}")
#             return f"Error: {e}"

# import google.generativeai as genai
# import os
# from typing import Optional, List
# from dotenv import load_dotenv
# from pathlib import Path

# class GeminiClient:
#     def __init__(self, model_name: str = "gemini-2.5-flash", system_instruction: str = None):

#         # Load .env from project root
#         env_path = Path(__file__).resolve().parent.parent / ".env"
#         load_dotenv(dotenv_path=env_path, override=True)

#         api_key = os.getenv("GEMINI_API_KEY")

#         if not api_key:
#             print("WARNING: GEMINI_API_KEY is not set.")
#         else:
#             genai.configure(api_key=api_key)

#         self.model = genai.GenerativeModel(
#             model_name=model_name,
#             system_instruction=system_instruction
#         )

import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env properly
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

class GeminiClient:
    def __init__(self, model_name="gemini-1.5-flash", system_instruction=None):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in .env")

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction
        )

    def generate_content(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text  
        except Exception as e:
            return f"Error: {str(e)}"
    # For streaming, we could use generate_content(stream=True) if supported, 
    # but for structured interleaving (Story -> Image -> Narration), we'll orchestrate 
    # the discrete calls in series and stream the chunks via SSE to the client.
