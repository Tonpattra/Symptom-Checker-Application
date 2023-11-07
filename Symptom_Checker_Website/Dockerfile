FROM python:3.8-slim

WORKDIR /app
RUN apt-get update
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt
COPY ./data/ /app/data/
COPY ./templates/ /app/templates/

COPY ./main.py /app/

EXPOSE 800

CMD ["python3", "/app/main.py"]