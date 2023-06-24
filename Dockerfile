FROM python:3.9

WORKDIR /app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN apt update && apt install -y netcat-traditional

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

RUN sed -i 's/\r$//g' /app/entrypoint.sh &&\
    chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh", "python", "main.py"]