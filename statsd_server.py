import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 8125

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"[StatsD Mock] Сервер запущено. Слухаємо UDP на {UDP_IP}:{UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(1024)
    print(f"[StatsD Mock Отримано]: {data.decode('utf-8')}")
