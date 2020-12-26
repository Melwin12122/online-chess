import pygame
from chess.constants import WIDTH, HEIGHT, CELL_SIZE, BLACK, button_font, RED
from chess.board import Board
from sys import exit
import socket
from threading import Thread
from tkinter import *
from pickle import loads, dumps

pygame.init()


client = None


def click():
    global client, e_ip, root
    SERVER = e_ip.get()
    try:
        PORT = 5050
        ADDR = (SERVER, PORT)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        root.destroy()
    except:
        root.destroy()
        exit("Server Error!")


root = Tk()

Label(root, text="IP: ").grid(row=0, column=0)
e_ip = Entry(root, width=50)
e_ip.grid(row=0, column=1)
e_ip.insert(0, socket.gethostbyname(socket.gethostname()))


Button(root, text="Submit", command=click).grid(row=2, column=0)


root.mainloop()


FPS = 60

# Fonts
font = pygame.font.SysFont("comicsans", 20)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

clock = pygame.time.Clock()
clock.tick(FPS)

board = None

events = None

msg = None

colour = None

recv_colour = False

recv_start = False

piece = None

def recv_msg():
    global client, msg, colour, colour, recv_colour, recv_start, piece
    while True:
        if not recv_colour:
            colour = client.recv(1).decode('utf-8')
            recv_colour = True
        elif not recv_start:
            msg = client.recv(5)
            recv_start = True
        else:
            try:
                temp1 = client.recv(28)
                temp2 = loads(temp1)
                msg = temp2
            except:
                piece = temp1.decode('utf-8')
    

def text_objects(text, font, colour, pos):
    global WIN
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.center = pos
    WIN.blit(text_surface, text_rect)

def button(text, x, y, w, h, colour, active_colour, action=None):
    global events
    mouse = pygame.mouse.get_pos()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(WIN, active_colour, (x-4, y-4, w+10, h+10))
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and action is not None:
                action()

    else:
        pygame.draw.rect(WIN, colour, (x, y, w, h))


    text_objects(text, button_font, BLACK, ((x + (w // 2)), (y + (h // 2))))


    

def quit_game():
    pygame.quit()
    exit()

def main():
    global WIN, events, board, colour, msg, client, piece
    running = True
    done = None
    board = Board(colour)
    r1 = r2 = c2 = c1 = None

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                quit_game()
            if event.type == pygame.MOUSEBUTTONUP and colour == board.turn:
                pos = pygame.mouse.get_pos()
                col = pos[0] // CELL_SIZE
                row = pos[1] // CELL_SIZE
                moves = board.select(row, col)
                if board.pawn_promo is not None:
                    p = board.pawn_promo
                    p = (p + (" " * (28 - len(p)))).encode('utf-8')
                    client.send(p)
                    client.send(dumps(moves))
                    board.pawn_promo = None
                    r1 = r2 = c1 = c2 = None
                elif len(moves) == 2:
                    client.send(dumps(moves))
                    r1 = r2 = c1 = c2 = None
    
        if colour != board.turn and msg is not None:
            moves = msg
            r1, c1 = moves[0]
            r2, c2 = moves[1]
            r1 = 7 - r1
            r2 = 7 - r2
            c1 = 7 - c1
            c2 = 7 - c2
            if piece is not None:
                board.pawn_promo = piece.strip()
                board.select(r1, c1, False)
                board.select(r2, c2, False)
                piece = None
                board.pawn_promo = None
            else:
                board.select(r1, c1)
                board.select(r2, c2) 
            msg = None

        if done is None:
            done = board.draw(WIN, r1, c1, r2, c2)    
        elif done == 'cm' or done == 'sm':
            running = False
            return None

        pygame.display.update()



def wait():
    global events, WIN, msg, thread, font
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit_game()
                running = False

        WIN.fill(BLACK)

        text_objects("Waiting for a opponent...", font, RED, (WIDTH//2, HEIGHT//2))

        if msg is not None:
            msg = None
            main()

        pygame.display.update()


thread = Thread(target=recv_msg)
thread.start()
wait()

