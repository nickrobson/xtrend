#!/usr/bin/env python3

# main.py
# SENG3011 - Cool Bananas
#
# The main entry point into running the Django server, and starting the program.
# It updates the server when necessary, and allows the server to be accessed via the web.

'''
DO NOT REMOVE THIS FILE

It is used as the entry point for the project.

ONLY edit the run() function below.
'''

import json
import os
import os.path
import queue
import sys
import threading
import time

VERSION_FILE = '.version'
EXIT_QUEUE = queue.Queue()

def run_update_thread():

    if not os.path.exists(VERSION_FILE):
        return

    try:

        def check_update():
            new_hash = ''
            with open(VERSION_FILE, 'r') as f:
                response = json.load(f)
                new_hash = response['hash']
            return new_hash

        current_version = check_update() # get currently-running version

        while True:
            new_hash = check_update()
            if new_hash != current_version:
                current_version = new_hash
                print('Found new version -- restarting!')
                break
            time.sleep(30) # sleep and check 30 seconds later!

    finally:

        EXIT_QUEUE.put('exit')


update_thread = threading.Thread(name='Update Checker', target=run_update_thread, daemon=True)
update_thread.start()


def run_server_thread():

    '''
    Edit this function only! (everything else is part of the update checker)
    '''

    try:

        from django.core.management import execute_from_command_line

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seng.server.settings")

        if len(sys.argv[1:]):
            execute_from_command_line(['main.py'] + sys.argv[1:])
        else:
            execute_from_command_line(['main.py', 'runserver', '127.0.0.1:5002'])

    finally:

        EXIT_QUEUE.put('exit')


main_thread = threading.Thread(name='Main Thread', target=run_server_thread, daemon=True)
main_thread.start()

EXIT_QUEUE.get() # block until we get a QUIT status
time.sleep(1)
