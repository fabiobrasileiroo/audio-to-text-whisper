import whisper  # Importa o modelo Whisper para transcrição de áudio
import sys  # Módulo do sistema para capturar argumentos de linha de comando
import os  # Biblioteca para manipulação de arquivos e diretórios
import subprocess  # Permite executar comandos externos no sistema operacional
from fastapi import FastAPI, File, UploadFile  # Importa o FastAPI para criar a API e manipular uploads de arquivos
from pathlib import Path  # Manipulação de caminhos de arquivos

# Cria uma instância do FastAPI para definir os endpoints da API
app = FastAPI()

# Carrega um modelo do Whisper mais preciso para transcrição
# "medium" é mais preciso do que "base", mas pode ser mais lento
# "large" pode ser usado para máxima precisão, mas consome mais memória
model = whisper.load_model("medium")  

def extract_audio(video_path: str) -> str:
    """
    Extrai o áudio de um arquivo de vídeo MP4 e salva como WAV (16kHz, mono) para maior precisão.
    """
    audio_path = video_path.replace(".mp4", ".wav")
    
    command = [
        "ffmpeg", "-i", video_path, 
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path, "-y"
    ]
    
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    return audio_path

def transcribe_audio(audio_path: str) -> str:
    """
    Transcreve um arquivo de áudio e retorna o texto com alta precisão.
    """
    print(f"🔊 Transcrevendo o arquivo: {audio_path}")
    result = model.transcribe(audio_path, temperature=0, language="pt", word_timestamps=True)
    return result["text"]

@app.post("/transcribe")
async def transcribe_video(file: UploadFile = File(...)):
    """
    Endpoint para receber um vídeo MP4 via API e retornar a transcrição com alta precisão.
    """
    file_location = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())

    # Extrai áudio do vídeo
    audio_file = extract_audio(file_location)

    # Transcreve áudio extraído
    transcription = transcribe_audio(audio_file)

    # Remove arquivos temporários
    os.remove(file_location)
    os.remove(audio_file)

    return {"filename": file.filename, "transcription": transcription}

if __name__ == "__main__":
    # Rodar via terminal para arquivos locais
    if len(sys.argv) > 1:
        video_file = sys.argv[1]
        audio_file = extract_audio(video_file)
        transcription = transcribe_audio(audio_file)
        print("\n📝 Transcrição:\n")
        print(transcription)
    else:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)