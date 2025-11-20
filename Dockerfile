FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

RUN apt update && apt install -y python3 python3-pip ffmpeg

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt

CMD ["bash", "startup.sh"]
