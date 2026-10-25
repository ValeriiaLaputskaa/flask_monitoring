import time
import socket
import logging
from flask import Flask, jsonify

app = Flask(__name__)

# 1. Налаштування журналювання
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

start_time = time.time()
request_counter = 0

STATSD_IP = "127.0.0.1"
STATSD_PORT = 8125

def send_to_statsd(metric_message: str):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(metric_message.encode('utf-8'), (STATSD_IP, STATSD_PORT))
    except Exception as e:
        logging.warning(f"Не вдалося надіслати метрику в StatsD: {e}")

@app.before_request
def count_requests():
    global request_counter
    request_counter += 1

@app.route('/')
def home():
    logging.info("Отримано запит на головну сторінку /")
    return "Сервіс працює", 200

@app.route('/error')
def trigger_error():
    logging.warning("Маршрут /error викликано: спроба ділення на нуль")
    result = 1 / 0
    return str(result)

@app.route('/status')
def status():
    uptime_seconds = int(time.time() - start_time)
    logging.info(f"Отримано запит /status. Uptime: {uptime_seconds}s, Requests: {request_counter}")
    return jsonify({
        "status": "running",
        "uptime_seconds": uptime_seconds,
        "requests_handled": request_counter
    }), 200

@app.errorhandler(Exception)
def handle_exception(e):
    logging.exception(f"Виникла неперехоплена помилка: {e}")
    send_to_statsd(f"errors.unhandled:1|c|error={type(e).__name__}")
    return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
