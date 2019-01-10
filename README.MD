NB: This project is currently undergoing refactoring and an upgrade as the codebase is from 2016
and there have been many improvements in the used libraries.

A quick to-do list:
- [COMPLETE] Implement a more robust multi-threaded framework for messaging
- Upgrade the SSL implementation
- Allow for management of multiple ARK Servers at the same time
- Quality of Life Improvements.

Requirements
------------

For server component...
Port 27888 TCP incoming

For server and client...
Python 3.4.3
https://www.python.org/downloads/release/python-343/

In file section, download "Windows x86-64 MSI installer".


Installation
------------

1. Install Python
a) Select a destination folder.
b) Customize the installation by adding the feature "Add python.exe to Path".
c) Continue the installation.

Once Python is installed, check if python folders were successfully added to PATH variable:
- Navigate to System Properties and click on Environment Variables...
- Add the following strings (change path name if you installed Python to a different folder) if not done by Python Installer.
C:\Python34
C:\Python34\Scripts

2. Install Colorama
a) Open a DOS prompt.
b) Run the following command...
pip install colorama


Usage
-----

For servers...
Run the sockserv.py file and your ARK Automation server should be running, it will also
create a Transactions.log to keep track of who has been connecting and doing what.

For clients...
Run the sockcli.py file. Possible commands are listed in the window. Just type in an appropriate number.


######IMPORTANT######
Keep the crt folder in the same directory as sockserv.py and sockcli.py otherwise the SSL will fail.
