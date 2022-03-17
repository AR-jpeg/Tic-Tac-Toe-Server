from random import randrange
from typing import List
from time import sleep
import threading
import socket

from game import (
    Game, Player,
    Point, GameOptions
)

# Setup the globals vars for the socket to connect to
IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (IP, PORT)

HEADER_LENGTH = 8
DECODE_FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!DISCONNECT!"
DELAY = 5

active_games: List[Game] = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def sendMsg(msg: str, conn: socket.socket, number_of_msgs_expecting: int=0):
    
    msg = msg.encode(DECODE_FORMAT)
    msg_length = str(len(msg)).encode(DECODE_FORMAT)
    number_of_msgs_to_recv = str(number_of_msgs_expecting).encode(DECODE_FORMAT)

    # Pad the message length to be HEADER_LENGTH chars long
    msg_length += b" " * (HEADER_LENGTH-len(msg_length))
    number_of_msgs_to_recv += b" " * (HEADER_LENGTH-len(number_of_msgs_to_recv))

    print(msg_length + number_of_msgs_to_recv + msg)

    conn.send(msg_length + number_of_msgs_to_recv + msg)


def reciveMsg(conn: socket.socket) -> str:
    msg_len = conn.recv(HEADER_LENGTH).decode(DECODE_FORMAT)

    if not msg_len:
        return

    msg_len = int(msg_len)
    msg = conn.recv(msg_len).decode(DECODE_FORMAT)

    return msg

def waitUntilGameHasMinPlayers(g: Game):
    while g.options.minSizeToWin != g.playersConnected:
        sleep(DELAY)

def handleGame(game: Game, conn: socket.socket):
    game.playersConnected += 1
    waitUntilGameHasMinPlayers(game)

    print("THERE ARE ENOUGH PLAYERS")

    # Once there are enough players, do smth :D



def handleClient(conn: socket.socket, addr):
    print(f"[NEW ACTIVE CONNECTION] Client at {addr} connected to the server, there is now {threading.activeCount() - 1} client(s) connected")
    
    sendMsg("Pls work", conn)
    sendMsg("No u", conn, 2)

    a = reciveMsg(conn)
    b = reciveMsg(conn)

    print(a,b)

    # connected = True
    # gameID = int(reciveMsg(conn))

    # print(gameID)
    # foundgameID = False

    # for game in active_games:
    #     if game.id == gameID:
    #         if game.playersConnected >= game.options.numberOfPlayers:
    #             sendMsg("Game already full. ", conn)
    #             conn.close()
            
    #         # Send to a pre-existing game
    #         handleGame(game, conn)
    #         foundgameID = True

    # print(foundgameID)

    # if not foundgameID:
    #     sendMsg(f"Couldn't find a game with the ID {gameID}, do you want to create a new game?", conn)

    #     if bool(reciveMsg(conn)):
    #         while gameID := randrange(1, 1000):
    #             print(f"TRYING GAME ID {gameID}")
    #             for _g in active_games:
    #                 if _g.id == gameID:
    #                     continue

    #         sendMsg(f'Creating a new game with the ID {gameID}')
    #     else:
    #         conn.close()
    #         return


    # print("thing")

    # # Get the game options from the client
    # name, symbol = reciveMsg(conn), reciveMsg(conn)
    # playersToStart = int(reciveMsg(conn))
    # minSizeToWin = int(reciveMsg(conn))
    # boardSize = int(reciveMsg(conn))
    # empty = reciveMsg(conn)

    # gameOptions = GameOptions(
    #     [Player(name, symbol)],
    #     playersToStart,
    #     minSizeToWin,
    #     boardSize,
    #     empty
    # )

    # # Create a new game
    # active_games.append(Game(gameOptions, gameID))
    
    # print(active_games)

    # # Send client to a pre-existing game (that was just created)
    # handleGame(gameID, conn)

    # while connected:
    #     msg = reciveMsg(conn)

    #     if msg == DISCONNECT_MESSAGE:
    #         print(f"[CLIENT DISCONNECT] Client at {addr} just disconnected cleanly, closing conncetion")
    #         print(f"[ACTIVE CONNECTION] There are now {threading.activeCount()-2} active connections")
    #         connected = False

    #     sendMsg(f"You sent the msg: {msg}", conn)
    
    # conn.close()

print(f"[STARTING] Starting the server at addr {IP}:{PORT}")
server.listen()

while True: 
    # Always look for new threads, and pass them off to handleClient
    conn, addr = server.accept()
    thread = threading.Thread(target=handleClient, args=(conn, addr))
    thread.start()
