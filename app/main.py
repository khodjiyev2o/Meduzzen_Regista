
from os import getenv
from fastapi import FastAPI
from uvicorn import run as startserver
from .config import configure
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
configure(app)


@app.get('/', status_code=200)
async def root():
    return {"status": "Working from CI/CD GitHub actions by Samandar Khodjiyev for Meduzzen!"}


if __name__ == '__main__':
    startserver('main:app', host=getenv('APP_HOST'), port=int(getenv('APP_PORT')), reload=True) 