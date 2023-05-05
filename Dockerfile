FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/bot

WORKDIR /bot/

COPY . /bot

RUN apt-get update -y

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "bot"]
