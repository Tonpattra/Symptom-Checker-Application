FROM python:3.8-slim

WORKDIR /app
RUN apt-get update
COPY . .
RUN pip install -r requirement.txt

EXPOSE 5000

CMD ["python3", "/app/model_caller.py"]