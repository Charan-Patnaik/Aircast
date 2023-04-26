FROM python:3.10.6


# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     git \
#     && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

WORKDIR /frontend

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "Login.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableWebsocketCompression=false"]