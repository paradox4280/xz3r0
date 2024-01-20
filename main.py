import requests

from dotenv import dotenv_values
from dataclasses import dataclass
from bottle import Bottle, request, run


@dataclass
class Config:
    CHAT_ID: str | None
    BOT_TOKEN: str | None


config = Config(**dotenv_values('.env'))

app = Bottle()


@app.route('/ping', method='GET')
def ping():
    return {'message': 'ok'}


@app.route('/myip', method='GET')
def show_ip() -> dict[str, str]:
    return {'my_ip': request.environ.get('REMOTE_ADDR')}


@app.route('/notify', method='POST')
def notify() -> None:
    message = request.body.read().decode('ascii')
    params = {'chat_id': config.CHAT_ID,'text': message}
    url = f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage?{params}'
    requests.get(url, data=params)


if __name__ == '__main__':
    run(app, host='localhost', debug=False)