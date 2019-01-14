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


# def serverstatus():
#     global serverstate
#     tasklistr = os.popen("tasklist").read()
#     if "ShooterGameServer.exe" in tasklistr:
#         serverstate = True
#         print("Server Status is Running")
#         with open("Transactions.txt", "a") as w1:
#             w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Server Status is Running")
#     else:
#         serverstate = False
#         print("Server Status is Stopped")
#         with open("Transactions.txt", "a") as w1:
#             w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Server Status is Stopped")




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

# def clientthread(connstream):
#     connstream.send(b'Welcome to the server! We are running version 0.3.2.')
#
#     while True:
#         data = connstream.recv(1024)
#         global serverstate
#
#         # Start The Center
#         if data == (b"start1"):
#             serverstatus()
#             updatestatus()
#             if serverstate is False and updatestate is False:
#                 print("Starting Server The Center")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Starting Server The Center")
#                 subprocess.Popen(
#                     'C:\ARK\ARKServer 3\ShooterGame\Binaries\Win64\ShooterGameServer.exe "TheCenter?MaxPlayers=20?listen" -log -NoBattlEye')
#                 connstream.sendall(b"ARK Server - The Center is being started")
#             elif serverstate == True:
#                 print("Server is already running")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Server is already running")
#                 connstream.sendall(b"Server is already running")
#             elif updatestate == True:
#                 print("Update is still in progress")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Update is still in progress")
#                 connstream.sendall(b"Server update is still in progress")
#
#         # Start Scorched Earth
#         elif data == (b"start2"):
#             serverstatus()
#             updatestatus()
#             if serverstate is False and updatestate is False:
#                 print("Starting Server Scorched Earth")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Starting Server Scorched Earth")
#                 subprocess.Popen(
#                     'C:\ARK\ARKServer 2\ShooterGame\Binaries\Win64\ShooterGameServer.exe "ScorchedEarth_P?MaxPlayers=20?listen" -log -NoBattlEye')
#                 connstream.sendall(b"ARK Server - Scorched Earth is being started")
#             elif serverstate == True:
#                 print("Server is already running")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Server is already running")
#                 connstream.sendall(b"Server is already running")
#             elif updatestate == True:
#                 print("Update is still in progress")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Update is still in progress")
#                 connstream.sendall(b"Server update is still in progress")
#
#         # Stop server
#         elif data == (b"stop"):
#             serverstatus()
#             updatestatus()
#             if serverstate == False:
#                 print("Server is already stopped")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Server is already stopped")
#                 connstream.sendall(b"Server is already stopped")
#             elif serverstate == True:
#                 print("Server is being stopped")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Server is being stopped")
#                 os.system("taskkill /im ShooterGameServer.exe /f")
#                 connstream.sendall(b"Server is being stopped")
#
#         # Update The Center
#         elif data == (b"update1"):
#             serverstatus()
#             updatestatus()
#             if serverstate is False and updatestate is False:
#                 print("Updating Server The Center")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Updating Server The Center")
#                 subprocess.Popen('C:\ARK\ARK Server Launcher\SteamCMD\SteamCMD.exe +runscript tc.txt')
#                 connstream.sendall(b"ARK Server - The Center is being updated")
#             elif serverstate == True:
#                 print("Server is still running. Cannot update.")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime(
#                         "%Y-%m-%d %H:%M:%S") + " Server is still running. Cannot update.")
#                 connstream.sendall(b"Server needs to be stopped in order to update it!")
#             elif updatestate == True:
#                 print("Another update is still running. Cannot continue.")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime(
#                         "%Y-%m-%d %H:%M:%S") + " Another update is still running. Cannot continue.")
#                 connstream.sendall(b"Another update is already in progress!")
#
#         # Update Scorched Earth
#         elif data == (b"update2"):
#             serverstatus()
#             updatestatus()
#             if serverstate is False and updatestate is False:
#                 print("Updating Server Scorched Earth")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Updating Server Scorched Earth")
#                 subprocess.Popen('C:\ARK\ARK Server Launcher\SteamCMD\SteamCMD.exe +runscript se.txt')
#                 connstream.sendall(b"ARK Server - Scorched Earth is being updated")
#             elif serverstate == True:
#                 print("Server is still running. Cannot update.")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime(
#                         "%Y-%m-%d %H:%M:%S") + " Server is still running. Cannot update.")
#                 connstream.sendall(b"Server needs to be stopped in order to update it!")
#             elif updatestate == True:
#                 print("Another update is still running. Cannot continue.")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime(
#                         "%Y-%m-%d %H:%M:%S") + " Another update is still running. Cannot continue.")
#                 connstream.sendall(b"Another update is already in progress!")
#
#         # Status check
#         elif data == (b"status"):
#             serverstatus()
#             updatestatus()
#             if updatestate == True:
#                 print("Update in progress.")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Update in progress.")
#                 connstream.sendall(b"Update in progress...")
#             elif serverstate == False:
#                 print("Server is stopped")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Server is stopped")
#                 connstream.sendall(b"Server is stopped.")
#             elif serverstate == True:
#                 print("Server is running")
#                 with open("Transactions.txt", "a") as w1:
#                     w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Server is running")
#                 connstream.sendall(b"Server is running.")
#
#         if not data:
#             break
#
#     connstream.close()
#     print("Connection with " + fromaddr[0] + ":" + str(fromaddr[1]) + " closed")
#     with open("Transactions.txt", "a") as w1:
#         w1.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Connection with " + fromaddr[0] + ":" + str(
#             fromaddr[1]) + " closed")
#
#


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
