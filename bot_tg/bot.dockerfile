FROM python:3.10.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONDONTBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD [ "python", "run.py" ]