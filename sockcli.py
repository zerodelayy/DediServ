# Version 0.8.0

import socket
import sys
import encodings
import os
import ssl
import traceback
import selectors

import libclient

sel = selectors.DefaultSelector()

if os.path.isfile("Errors.txt") is True:
    sys.stderr = open("Errors.log", "a")
else:
    sys.stderr = open("Errors.log", "w")


server_commands = {
    0: ("status", "all"),
    1: ("start", "Island"),
    2: ("start", "Center"),
    3: ("start", "Scorched"),
    4: ("start", "Ragnarok"),
    5: ("start", "Aberration"),
    6: ("start", "Extinction"),
    7: ("kill", "Island"),
    8: ("kill", "Center"),
    9: ("kill", "Scorched"),
    10: ("kill", "Ragnarok"),
    11: ("kill", "Aberration"),
    12: ("kill", "Extinction"),
    13: ("update", "all"),
    14: ("update", "Ragnarok")
}


def create_request(action, value):
    # if action == "search":
    return dict(
        type="text/json",
        encoding="utf-8",
        content=dict(action=action, value=value),
    )
    # else:
    #     return dict(
    #         type="binary/custom-client-binary-type",
    #         encoding="binary",
    #         content=bytes(action + value, encoding="utf-8"),
    #     )


def start_connection(host, port, request):
    addr = (host, port)
    print("Starting Connection to {}".format(addr))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclient.Message(sel, sock, addr, request)
    sel.register(sock, events, data=message)


host, port = "127.0.0.1", 27888


def ark_command(action, command):
    action, value = action, command
    request = create_request(action, value)
    start_connection(host, port, request)
    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        "main: error: exception for",
                        f"{message.addr}:\n{traceback.format.exc()}",
                    )
                    message.close()
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("Keyboard interaction detected, exiting")



#
#
# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
# context.verify_mode = ssl.CERT_REQUIRED
# context.check_hostname = True
# context.load_verify_locations("crt/cert-20170526-150709.crt")

while True:
    print("Welcome to the ARK Server Remote Management Client!")
    print("---------------------------------------------------")
    print("Version 0.8.0")
    print("")
    while True:
        print("Please select one of the following options:")
        print("0.   Check status of ARK Server")
        print("")
        print("1.   Start ARK Server - The Island")
        print("2.   Start ARK Server - The Center")
        print("3.   Start ARK Server - Scorched Earth")
        print("4.   Start ARK Server - Ragnarok --with CKF MOD--")
        print("5.   Start ARK Server - Aberration (not clustered)")
        print("6.   Start ARK Server - Extinction")
        print("")
        print("7.   Stop ARK Server - The Island")
        print("8.   Stop ARK Server - The Center")
        print("9.  Stop ARK Server - Scorched Earth")
        print("10.  Stop ARK Server - Ragnarok --with CKF MOD--")
        print("11.  Stop ARK Server - Aberration (not clustered)")
        print("12.  Stop ARK Server - Extinction")
        print("")
        print("13.  Update ARK Server - All maps except Ragnarok")
        print("14.  Update ARK Server - Ragnarok")
        print("")
        print("")
        print("15.  Exit ARK Server Client")
        print("")
        print("")
        usrin = input("Option:  ")
        choice = server_commands.get(int(usrin))
        ark_command(choice[0], choice[1])
        input("Press ENTER to continue...")

        if usrin == "15":
            sel.close()
            sys.exit()

        if usrin == "16":
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

        if usrin == "17":
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




