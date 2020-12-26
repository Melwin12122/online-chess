import socket
from threading import Thread

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

players = []

def handle_client(conn, addr):
    # name = conn.recv(64).decode('utf-8')
    players.append(conn)
    connected = True
    print(addr, " joined.")
    try:
        while len(players) % 2 != 0:
            pass
        else:
            print("Started...")
            if conn == players[0]:
                conn.send('w'.encode('utf-8'))
            else:
                conn.send('b'.encode('utf-8'))
            conn.send("start".encode('utf-8'))
            while connected:
                msg = conn.recv(28)
                try:
                    piece = msg.decode('utf-8')
                    for player in players:
                        if player is not conn:
                            player.send(piece.encode('utf-8'))
                    msg = conn.recv(28)
                except:
                    pass
                for player in players:
                    if player is not conn:
                        player.send(msg)
    except:
        players.remove(conn)
        print(addr, " left.")


        

def start():
    server.listen(2)
    while True:
        conn, addr = server.accept()
        thread = Thread(target=handle_client, args=(conn, addr))
        thread.start()

start()

