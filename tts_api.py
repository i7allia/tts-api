# 1. Создай файл tts_api.py
cat > tts_api.py << 'EOF'
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "TTS API работает!"}

@app.get("/tts")
async def text_to_speech(text: str = "Hello", lang: str = "en"):
    print(f"[TTS] Текст: '{text}'")
    
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    
    return Response(
        content=mp3_fp.read(),
        media_type="audio/mpeg",
        headers={"Content-Disposition": "attachment; filename=speech.mp3"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
EOF
