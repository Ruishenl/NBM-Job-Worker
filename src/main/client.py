import socket
import time
import json


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


# Trying to simulate for very simple a job assigning process here; in real case i assume message will be coming from
# sth like sqs or api
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    job_1 = {'job_id': 1, 'job_desc': 'first', 'hrs_required': 20}
    job_2 = {'job_id': 2, 'job_desc': 'second', 'hrs_required': 10}
    job_3 = {'job_id': 3, 'job_desc': 'third', 'hrs_required': 3}
    job_4 = {'job_id': 4, 'job_desc': 'fourth', 'hrs_required': 12}
    job_5 = {'job_id': 5, 'job_desc': 'fifth', 'hrs_required': 10}


    s.sendall(json.dumps(job_1).encode('utf-8'))
    time.sleep(10)
    data = s.recv(1024)
    print(data)

    s.sendall(json.dumps(job_2).encode('utf-8'))
    time.sleep(3)
    data = s.recv(1024)
    print(data)

    s.sendall(json.dumps(job_3).encode('utf-8'))
    time.sleep(5)
    data = s.recv(1024)
    print(data)


    s.sendall(json.dumps(job_4).encode('utf-8'))
    time.sleep(2)
    data = s.recv(1024)
    print(data)

    s.sendall(json.dumps(job_5).encode('utf-8'))
    data = s.recv(1024)
    print(data)
