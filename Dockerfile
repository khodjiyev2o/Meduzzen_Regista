FROM --platform=linux/amd64 python:3.9.7
RUN pip install --upgrade pip
WORKDIR /api

COPY requirements.txt ./


RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0","--reload"]