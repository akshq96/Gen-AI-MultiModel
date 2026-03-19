"use client";

import { useState, useRef, useEffect } from "react";
import { Sparkles, Image as ImageIcon, Mic, Clapperboard, Loader2 } from "lucide-react";

type StreamChunk = {
  type: string;
  data: any;
};

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [imageRef, setImageRef] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [status, setStatus] = useState("Waiting for input...");
  const [blocks, setBlocks] = useState<StreamChunk[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll as new interleaved elements arrive
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [blocks]);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    
    setIsGenerating(true);
    setBlocks([]);
    setStatus("Connecting to AI Studio...");

    try {
      const response = await fetch("http://localhost:8000/generate-story", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, image_reference: imageRef }),
      });

      if (!response.body) throw new Error("No readable stream");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const parsed: StreamChunk = JSON.parse(line.replace("data: ", ""));

              if (parsed.type === "status") {
                setStatus(parsed.data);
              } else if (parsed.type === "done") {
                setIsGenerating(false);
              } else {
                // Add interleaved content blocks as they arrive
                setBlocks((prev) => [...prev, parsed]);
              }
            } catch (e) {
              console.error("Error parsing SSE JSON", e);
            }
          }
        }
      }
    } catch (error) {
      console.error(error);
      setStatus("Error generating experience.");
      setIsGenerating(false);
    }
  };

  return (
    <main className="min-h-screen p-8 flex flex-col items-center">
      <header className="text-center mb-12">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent mb-4">
          Creative Director AI
        </h1>
        <p className="text-slate-400 max-w-2xl mx-auto">
          Write a prompt. Our multimodal agent will orchestrate a story, illustrate it, provide audio scripts, and build a video storyboard.
        </p>
      </header>

      <div className="w-full max-w-3xl studio-card mb-8">
        <div className="flex flex-col gap-4">
          <textarea
            className="studio-input min-h-[120px]"
            placeholder="e.g. Create a short story explaining black holes for children..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            disabled={isGenerating}
          />
          <input
            type="text"
            className="studio-input"
            placeholder="Optional: Paste a reference image URL to guide the story..."
            value={imageRef}
            onChange={(e) => setImageRef(e.target.value)}
            disabled={isGenerating}
          />
          <div className="flex items-center justify-between mt-2">
            <div className="flex items-center gap-2 text-sm text-slate-400">
              {isGenerating && <Loader2 className="w-4 h-4 animate-spin" />}
              <span>{status}</span>
            </div>
            <button
              className="studio-button flex items-center gap-2"
              onClick={handleGenerate}
              disabled={isGenerating || !prompt.trim()}
            >
              <Sparkles className="w-5 h-5" />
              {isGenerating ? "Generating..." : "Generate Experience"}
            </button>
          </div>
        </div>
      </div>

      {/* Interleaved Rendering Area */}
      {blocks.length > 0 && (
        <div className="interleaved-container">
          <div className="flex items-center justify-center mb-4">
            <span className="h-px bg-slate-700 w-full"></span>
            <span className="px-4 text-xs font-semibold text-slate-500 uppercase tracking-widest whitespace-nowrap">
              Interleaved Output Stream
            </span>
            <span className="h-px bg-slate-700 w-full"></span>
          </div>

          {blocks.map((block, idx) => (
            <div key={idx}>
              {/* Story Text Block */}
              {block.type === "story" && (
                <div className="content-block block-story">
                  <p className="whitespace-pre-wrap">{block.data}</p>
                </div>
              )}

              {/* Image Illustration Block */}
              {block.type === "image_prompt" && (
                <div className="content-block block-image">
                  <ImageIcon className="w-12 h-12 text-blue-400 mb-4 opacity-75" />
                  <p className="text-blue-200 text-sm max-w-xl italic mb-2">
                    " {block.data} "
                  </p>
                  <span className="text-xs text-blue-400/60 uppercase font-semibold">
                    Illustration Prompt Generated Ready for Cloud Storage
                  </span>
                </div>
              )}

              {/* Narration Output Block */}
              {block.type === "narration" && (
                <div className="content-block block-narration">
                  <div className="flex items-center gap-3 mb-3 border-b border-purple-800/50 pb-2">
                    <Mic className="w-5 h-5 text-purple-400" />
                    <h3 className="text-sm font-bold uppercase tracking-wider text-purple-300">
                      Voiceover Script
                    </h3>
                  </div>
                  <p className="whitespace-pre-wrap">{block.data}</p>
                </div>
              )}

              {/* Storyboard Block */}
              {block.type === "storyboard" && (
                <div className="content-block block-storyboard">
                  <div className="flex items-center gap-3 mb-3 border-b border-emerald-800/50 pb-2">
                    <Clapperboard className="w-5 h-5 text-emerald-400" />
                    <h3 className="text-sm font-bold uppercase tracking-wider text-emerald-300">
                      Video Storyboard
                    </h3>
                  </div>
                  <p>{block.data}</p>
                </div>
              )}
            </div>
          ))}
          <div ref={bottomRef} className="h-4" />
        </div>
      )}
    </main>
  );
}
