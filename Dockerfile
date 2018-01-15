FROM python:3.5-alpine
RUN ["mkdir","/app"]
WORKDIR /app
COPY requirements.txt .
RUN ["pip","install","--no-cache-dir","-r","requirements.txt"]
ADD src/*.py ./
CMD ["./main.py"]
