FROM python:3.10-slim

WORKDIR /app

RUN apt update && apt install -y ffmpeg

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["uvicorn","transcriber:app","--host","0.0.0.0","--port","8000"]