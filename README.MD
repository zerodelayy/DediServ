Version 0.8.8
-----
Refactoring has been completed, but SSL implementation is still pending. Codebase is ready to be used.

A quick to-do list:
- [COMPLETE] Implement a more robust multi-threaded framework for messaging
- Upgrade the SSL implementation
- [COMPLETE] Allow for management of multiple ARK Servers at the same time
- [COMPLETE] Quality of Life Improvements.

Requirements
------------

For server component...

Port 27888 TCP incoming (port can be changed)

For server and client...

Python 3.7.2

psutil




Usage
-----

For servers...
Run the sockserv.py file and your ARK Automation server should be running, it will also
create a Transactions.log to keep track of who has been connecting and doing what.
If you want to modify the launch commands, please refer to the dictionary in libserv.py.

For clients...
Run the sockcli.py file. Possible commands are listed in the window. Just type in an appropriate number.


######IMPORTANT######
-----
Keep the crt folder in the same directory as sockserv.py and sockcli.py otherwise the SSL will fail.
