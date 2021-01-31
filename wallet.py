import socket
import sys
import threading

host = socket.gethostname()
q = sys.argv[1]
port = sys.argv[-1]
# First, wallet establish a connection to a node
# Then 
def receiving(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, 10000))
    s.connect((host, int(port)))
    msg = s.recv(1024).decode('utf-8')
    if len(msg) > 0:
        print(msg)
        s.shutdown(socket.SHUT_RDWR)
        s.close()
    return

def sending(msg, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s_c.bind((host, 10001))
    s_c.connect((host, int(port)))
    s_c.shutdown(socket.SHUT_RDWR)
    s_c.close()
    s.bind((host, 10002))
    s.listen(1)
    while True:
        connection, addr = s.accept()
        connection.send(bytes(msg, 'utf-8'))
        print(f'I send the message')
        return

if q == 'consult':
    receiving(int(port))
elif q == 'chat':
    msg = input('Your message:')
    sending(msg, int(port))
