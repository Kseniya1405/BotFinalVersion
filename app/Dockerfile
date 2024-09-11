FROM python:3.10

WORKDIR /app

COPY config/requirements.txt ./config/

RUN pip install --no-cache-dir -r config/requirements.txt

COPY . .

CMD ["python", "main.py"]