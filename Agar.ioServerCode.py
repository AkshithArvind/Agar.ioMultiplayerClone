import socket
import threading
import random
import ast

# TECH WITH TIM'S CODE FOLLOWING, WITH SOME EDITS FROM ME, WHICH CAN BE FOUND AT
# https://www.techwithtim.net/tutorials/socket-programming/
HEADER = 64
PORT = 6668
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
players = {}
blobs = []
for _ in range(20):
    blobs.append([random.randint(0, 500), random.randint(0, 350)])
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    players[f'{conn} {addr}'] = [color, random.randint(10, 490), random.randint(10, 340), 10]
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            #MY CODE FOLLOWING
            if msg == 'DOWN':
                old = players[f'{conn} {addr}']
                if old[2] < 350:
                    old[2] += 5
                players[f'{conn} {addr}'] = old
            if msg == 'UP':
                old = players[f'{conn} {addr}']
                if old[2] > 0:
                    old[2] -= 5
                players[f'{conn} {addr}'] = old
            if msg == 'RIGHT':
                old = players[f'{conn} {addr}']
                if old[1] < 500:
                    old[1] += 5
                players[f'{conn} {addr}'] = old
            if msg == 'LEFT':
                old = players[f'{conn} {addr}']
                if old[1] > 0:
                    old[1] -= 5
                players[f'{conn} {addr}'] = old
            if msg.startswith('COLLISION '):
                old = players[f'{conn} {addr}']
                old[3] += 3
                blobs.remove(ast.literal_eval(msg.split(' ')[1]))
                blobs.append([random.randint(0, 500), random.randint(0, 350)])
            conn.sendall(str([players, blobs]).encode(FORMAT))
    conn.close()


#TECH WITH TIM'S CODE FOLLOWING

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
