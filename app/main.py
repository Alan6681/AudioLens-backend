from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import audio, summaries

app = FastAPI(
    title="AudioLens API",
    description="Turn audio lectures into detailed summaries",
    version="1.0.0",
)

# Allow your Vite frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "https://audio-lens-v1.vercel.app",
        "http://localhost:3000" 
    ], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(audio.router)
app.include_router(summaries.router)

@app.get("/")
def root():
    return {"message": "Welcome to AudioLens API 🎙️"}

@app.get("/health")
def health():
    return {"status": "ok"}