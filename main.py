import requests
import datetime

from dotenv import dotenv_values
from dataclasses import dataclass
from bottle import Bottle, request, run


@dataclass
class Config:
    CHAT_ID: str | None
    BOT_TOKEN: str | None


start_time = datetime.datetime.utcnow()
config = Config(**dotenv_values('.env'))

app = Bottle()


@app.route('/', method='GET')
@app.route('/health', method='GET')
def health():
    uptime = datetime.datetime.utcnow() - start_time
    return {'status': 'UP', 'uptime': str(uptime).split('.')[0]}


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
    run(app, host='0.0.0.0', port=8182, debug=False)