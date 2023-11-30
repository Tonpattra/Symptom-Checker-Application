FROM python:3.8-slim
WORKDIR /app
RUN apt-get update
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt
COPY . /app/
EXPOSE 8000
CMD ["python3", "/app/main.py"]