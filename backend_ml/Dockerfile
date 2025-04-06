FROM python:3.10

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirments.txt ./

RUN pip install --no-cache-dir -r requirments.txt

COPY . .

EXPOSE 5001

CMD ["python", "main.py"]