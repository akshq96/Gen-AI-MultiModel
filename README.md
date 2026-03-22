# Multimodal Creative Director AI (Next-Generation)

This project is a high-performance **Multimodal Creative Storytelling Agent** built to leverage Google Gemini models and Google Cloud via the GenAI SDK. It moves beyond standard text output by utilizing Server-Sent Events (SSE) to generate an interleaved multimedia stream:

1. **Text Paragraphs** (Story narrative)
2. **Generative Layout Prompts** (Images)
3. **Audio Scripts** (Voiceover Narration)
4. **Video Storyboards** (For AI Video Generators like Sora/Veo)

## Architecture

![Architecture](https://via.placeholder.com/800x400?text=Next.js+Frontend

*   **Frontend**: Built with `Next.js 14` and `Tailwind CSS`. Features a "studio" UI that consumes real-time data chunks to display interleaved content without waiting for the complete payload.
*   **Backend**: A `FastAPI` Server providing an asynchronous SSE (Server-Sent Events) endpoint (`/generate-story`), yielding segments dynamically.
*   **Agent Logic**: Distinct generators (`story`, `image`, `narration`, `storyboard`) powered by `gemini-2.5-flash` via the `google-generativeai` SDK.
*   **Media Storage (GCS Setup)**: The `media_storage.py` service outlines integration with Google Cloud Storage for handling generated image artifacts and returning Google-hosted URLs.

---

## 🚀 Local Development Setup

### 1. Requirements
*   Python 3.10+
*   Node.js v18+
*   A `GEMINI_API_KEY` from Google AI Studio.

### 2. Backend Setup
1. Open a terminal in the project root:
   ```bash
   cd multimodal-creative-agent
   pip install -r requirements.txt
   ```
2. Set up your `.env` file:
   ```bash
   cp .env.example .env
   # Add your GEMINI_API_KEY inside .env
   ```
3. Run the FastAPI server:
   ```bash
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   *The API will be available at `http://localhost:8000`.*

### 3. Frontend Setup
1. Open a new terminal tab and navigate to the frontend folder:
   ```bash
   cd multimodal-creative-agent/frontend
   npm install
   ```
2. Start the Next.js development server:
   ```bash
   npm run dev
   ``` 
   *The UI will be accessible at `http://localhost:3000`.*

---

## ☁️ Deploying to Google Cloud Run

To deploy this hackathon project, follow these steps:

1. **Containerize the Applications**
    *   Create a `Dockerfile` for the Python Backend.
    *   Create a `Dockerfile` for the Next.js Frontend.
2. **Authenticate with Google Cloud**
    ```bash
    gcloud auth login
    gcloud config set project YOUR_PROJECT_ID
    ```
3. **Deploy Backend (FastAPI)**
    ```bash
    gcloud run deploy creative-agent-backend \
      --source . \
      --set-env-vars GEMINI_API_KEY="YOUR_KEY_HERE" \
      --allow-unauthenticated \
      --region us-central1
    ```
    *Note the resulting Cloud Run URL and ensure it handles CORS properly for your frontend origin.*
4. **Deploy Frontend (Next.js)**
    Ensure the `API_URL` inside `app/page.tsx` is toggled to point to your new Cloud Run Backend URL instead of `localhost:8000`.
    ```bash
    cd frontend
    gcloud run deploy creative-agent-frontend \
      --source . \
      --allow-unauthenticated \
      --region us-central1
    ```
---

## ⚙️ Tech Stack

### Backend
- Python  
- FastAPI (or similar framework)  
- Gemini API (for AI generation)  

### Frontend
- Next.js  
- React  
- Tailwind CSS (assumed)  

---
## Hackathon Features Achieved
✅ **Multimodal Inputs**: Accepts text prompts and reference image URLs.
✅ **Interleaved Response Streaming**: Native UI experience showcasing Story $\\rightarrow$ Art $\\rightarrow$ Voice $\\rightarrow$ Video chunks dynamically.
✅ **Google GenAI SDK**: Implemented `gemini-2.5-flash` natively.
✅ **Google Cloud Integration**: Configured paths for Google Cloud Storage and designed for GCP Cloud Run deployment.
