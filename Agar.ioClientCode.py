import pygame
import socket
import time
import ast
import random

# TECH WITH TIM'S CODE FOLLOWING, WITH SOME EDITS FROM ME, WHICH CAN BE FOUND AT
# https://www.techwithtim.net/tutorials/socket-programming/

HEADER = 64
PORT = 6668
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    return ast.literal_eval(str(client.recv(2048).decode(FORMAT)))


# MY CODE FOLLOWING

pygame.init()
scr = pygame.display.set_mode((500, 350))
pygame.display.set_caption('Agar.io Clone')
run = True
direction = None
delay = 0.1
collision = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = 'LEFT'
            if event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
            if event.key == pygame.K_UP:
                direction = 'UP'
            if event.key == pygame.K_DOWN:
                direction = 'DOWN'
    scr.fill((255, 255, 255))
    if not collision:
        if direction is not None:
            n = send(direction)
            players = n[0]
            blobs = n[1]
            for y in blobs:
                circ = pygame.draw.circle(scr, (random.choice([0, 128, 200]), random.choice([0, 128, 200]), random.choice([0, 128, 200])), (y[0], y[1]), 1)
            values = list(players.values())
            for x in values:
                pygame.draw.circle(scr, x[0], (x[1], x[2]), x[3])
            pygame.display.update()
    else:
        send('COLLISION')
        collision = False
        direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    time.sleep(delay)
    pygame.display.update()
print('You left the game')
pygame.quit()
quit()
