# Version 0.3.2

import socket
import sys
import encodings
import os
import ssl
from colorama import Fore, Back, Style
from colorama import init

init()
if os.path.isfile("Errors.txt") is True:
    sys.stderr = open("Errors.log", "a")
else:
    sys.stderr = open("Errors.log", "w")


context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_verify_locations("crt/cert-20170526-150709.crt")

while True:
    print("Welcome to the ARK Server Remote Management Client!")
    print("---------------------------------------------------")
    print("Version 0.3.2")
    print("")
    while True:
        print("Please select one of the following options:")
        print("")
        print("1. Start ARK Server - The Center")
        print("2. Start ARK Server - Scorched Earth")
        print("")
        print("3. Stop ARK Server")
        print("")
        print("4. Update ARK Server - The Center")
        print("5. Update ARK Server - Scorched Earth")
        print("")
        print("6. Check status of ARK server")
        print("")
        print("")
        usrin = input("Option:  ")

        # Start The Center
        if usrin == "1":
            conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname="ark.com")
            conn.connect(("127.0.0.1", 27888))
            print(Fore.GREEN + conn.recv(1024).decode("utf-8"))
            conn.send(b"start1")
            print("")
            print(Fore.GREEN + conn.recv(1024).decode("utf-8"))
            print(Fore.RESET)
            conn.close()

        # Start Scorched Earth
        if usrin == "2":
            conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname="ark.com")
            conn.connect(("127.0.0.1", 27888))
            print(Fore.GREEN + conn.recv(1024).decode("utf-8"))
            conn.send(b"start2")
            print("")
            print(Fore.RED + conn.recv(1024).decode("utf-8"))
            print(Fore.RESET)
            conn.close()

        # Stop server
        if usrin == "3":
            conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname="ark.com")
            conn.connect(("127.0.0.1", 27888))
            print(Fore.GREEN + conn.recv(1024).decode("utf-8"))
            conn.send(b"stop")
            print("")
            print(Fore.RED + conn.recv(1024).decode("utf-8"))
            print(Fore.RESET)
            conn.close()

        # Update The Center
        if usrin == "4":
            conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname="ark.com")
            conn.connect(("127.0.0.1", 27888))
            print(Fore.GREEN + conn.recv(1024).decode("utf-8"))
            conn.send(b"update1")
            print("")
            print(Fore.BLUE + conn.recv(1024).decode("utf-8"))
            print(Fore.RESET)
            conn.close()

        # Update Scorched Earth
        if usrin == "5":
            conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname="ark.com")
            conn.connect(("127.0.0.1", 27888))
            print(Fore.GREEN + conn.recv(1024).decode("utf-8"))
            conn.send(b"update2")
            print("")
            print(Fore.BLUE + conn.recv(1024).decode("utf-8"))
            print(Fore.RESET)
            conn.close()

        # Status check
        if usrin == "6":
            conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname="ark.com")
            conn.connect(("127.0.0.1", 27888))
            print(Fore.GREEN + conn.recv(1024).decode("utf-8"))
            conn.send(b"status")
            print("")
            print(Fore.YELLOW + conn.recv(1024).decode("utf-8"))
            print(Fore.RESET)
            conn.close()

        if usrin == "7":
            print("                {")
            print('             }   }   {')
            print('            {   {  }  }')
            print('             }   }{  {')
            print('           _{  }{  }  }_')
            print('          (  }{  }{  {  )')
            print('          |""---------""| ')
            print('          |             /""\\')
            print('          |            | _  |')
            print('          |             / | |')
            print('          |             |/  |')
            print('          |             /  / ')
            print('          |            |  / ')
            print('          |            "T"')
            print('           ""---------""')
            print('COFFEE')
            print('IS')
            print('SERVED!')
            print('')
        if usrin == "8":
            print('             .---------------------------.')
            print('            /_   _   _         __  __   /|')
            print('           // \ / \ / \ |_/ | |_  (_   / |')
            print('          / \_  \_/ \_/ | \ | |__ ,_/ /  |')
            print('         :.__________________________/   /')
            print('         |  .--. .--.   .--.   .--.  |  /')
            print('         | (    )    ) (    ) (    ) | /')
            print("         |  '--' '--'   '--'   '--'  |/")
            print("         '---------------------------' ")
            print('YOUR COOKIES HAVE BEEN DONATED TO A CHARITY.')
            print('')
            print('THANK YOU FOR YOUR CHARITABLE DONATION.')
            print('')




