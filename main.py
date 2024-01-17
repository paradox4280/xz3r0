import urllib.parse
import urllib.request

from dotenv import dotenv_values
from fastapi import FastAPI, Body, status

config = {**dotenv_values('.env')}

app = FastAPI()


@app.get('/ping', status_code=status.HTTP_200_OK)
async def ping() -> dict[str, str]:
    return {'message': 'ok'}


@app.post('/notify', status_code=status.HTTP_200_OK)
async def notify(message: str = Body(...)) -> dict[str, str] | None:
    if len(message) > 2048:
        return {'error': 'message length greater then 2048'}
    params = urllib.parse.urlencode({'chat_id': config['CHAT_ID'],'text': message})
    url = f'https://api.telegram.org/bot{config["BOT_TOKEN"]}/sendMessage?{params}'
    with urllib.request.urlopen(url) as f:
        print(f.read().decode('ascii'))
