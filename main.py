from fastapi import FastAPI, Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import edge_tts
import os
import hashlib

app = FastAPI()

# Разрешаем запросы с любых сайтов
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "TTS API работает! Используйте GET /tts?text=Привет"}

@app.get("/tts")
async def text_to_speech(text: str = "Привет", voice: str = "ru-RU-SvetlanaNeural"):
    """Преобразование текста в речь"""
    try:
        # Создаем уникальное имя файла
        file_hash = hashlib.md5(f"{text}_{voice}".encode()).hexdigest()
        output_file = f"{file_hash}.mp3"
        
        # Очищаем старые файлы (не более 10)
        mp3_files = [f for f in os.listdir(".") if f.endswith(".mp3")]
        if len(mp3_files) > 10:
            for f in mp3_files[:-10]:
                try:
                    os.remove(f)
                except:
                    pass
        
        # Синтез речи
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        
        # Возвращаем файл
        return FileResponse(
            output_file,
            media_type="audio/mpeg",
            filename="speech.mp3"
        )
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/tts-get")
async def tts_get(text: str, voice: str = "ru-RU-SvetlanaNeural"):
    """Упрощенная версия (возвращает бинарные данные)"""
    try:
        communicate = edge_tts.Communicate(text, voice)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        return Response(content=audio_data, media_type="audio/mpeg")
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)