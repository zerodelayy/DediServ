# Version 1.0.0

import socket
import sys
import ssl
import os
from datetime import datetime
import selectors
import traceback
import libserver
import colorama
from colorama import Fore, Back, Style

sel = selectors.DefaultSelector()
colorama.init()

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print("Connected with " + addr[0] + ":" + str(addr[1]))
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)


if os.path.isfile("Transactions.txt") is True:
    with open("Transactions.txt", "a") as w1:
        w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " DediServ Socket Server has been started.")
else:
    with open("Transactions.txt", "w") as w1:
        w1.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " DediServ Socket Server has been started.")

HOST = '127.0.0.1'
PORT = 27888

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")
with open("Transactions.txt", "a") as w1:
    w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Socket created.")
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    lsock.bind((HOST, PORT))
except socket.error as msg:
    print("Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1])
    with open("Transactions.txt", "a") as w1:
        w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Bind failed. Error Code : " + str(
            msg[0]) + " Message " + msg[1])
    sys.exit()

lsock.listen()
lsock.setblocking(False)
print("Socket now listening")
with open("Transactions.txt", "a") as w1:
    w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Socket now listening")

sel.register(lsock, selectors.EVENT_READ, data=None)


try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        "main error: exception for",
                        f"{message.addr}:\n{traceback.format_exc()}",
                    )
                    message.close()
except KeyboardInterrupt:
    print("Keyboard interaction detected, exiting")
finally:
    sel.close()
