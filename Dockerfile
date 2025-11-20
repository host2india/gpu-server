#9) File: Dockerfile (optional)

#A minimal Dockerfile that installs Python and reqs; does not install GPU drivers. For GPU Docker, you must use NVIDIA base image.

# Dockerfile (cpu-friendly default)
FROM python:3.10-slim

WORKDIR /app

# OS deps (ffmpeg)
RUN apt-get update && apt-get install -y ffmpeg git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

