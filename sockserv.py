# Version 0.8.0

import socket
import sys
import ssl
import os
import subprocess
from datetime import datetime
import selectors
import traceback
import libserver
import signal

sel = selectors.DefaultSelector()







def accept_wrapper(sock):
    conn, addr = sock.accept()
    print("Connected with " + addr[0] + ":" + str(addr[1]))
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)


def serverstatus():
    global serverstate
    tasklistr = os.popen("tasklist").read()
    if "ShooterGameServer.exe" in tasklistr:
        serverstate = True
        print("Server Status is Running")
        with open("Transactions.txt", "a") as w1:
            w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Server Status is Running")
    else:
        serverstate = False
        print("Server Status is Stopped")
        with open("Transactions.txt", "a") as w1:
            w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Server Status is Stopped")




if os.path.isfile("Transactions.txt") is True:
    with open("Transactions.txt", "a") as w1:
        w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " ARK Socket Server has been started.")
else:
    with open("Transactions.txt", "w") as w1:
        w1.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " ARK Socket Server has been started.")

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



# context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# context.load_cert_chain(certfile="crt/cert-20170526-150709.crt", keyfile="crt/key-20170526-150709.pem")
#
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print("Socket created")
# with open("Transactions.txt", "a") as w1:
#     w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Socket created")
#
# try:
#     s.bind((HOST, PORT))
# except socket.error as msg:
#     print("Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1])
#     with open("Transactions.txt", "a") as w1:
#         w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1])
#     sys.exit()
#
# print("Socket bind complete")
# with open("Transactions.txt", "a") as w1:
#     w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Socket bind complete")
#
# s.listen(1)
# print("Socket now listening")
# with open("Transactions.txt", "a") as w1:
#     w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Socket now listening")
#
#
# while 1:
#
#     newsocket, fromaddr = s.accept()
#     print("Connected with " + fromaddr[0] + ":" + str(fromaddr[1]))
#     with open("Transactions.txt", "a") as w1:
#         w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Connected with " + fromaddr[0] + ":" + str(fromaddr[1]))
#     connstream = context.wrap_socket(newsocket, server_side=True, do_handshake_on_connect=True)
#     _thread.start_new_thread(clientthread ,(connstream,))
# s.close()
