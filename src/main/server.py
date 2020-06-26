import socket
import json
from src.worker.worker import assign_job
import time


HOST = "0.0.0.0"
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(0)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            job = json.loads(data.decode('utf-8'))
            assign_job(job)

            conn.sendall(b'recieved: %s}'%data)
        while True:
            time.sleep(10)
            print('sleep')
