#!/usr/bin/env python3

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

def thread_main():

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

update_thread = threading.Thread(name='Update Checker', target=thread_main, daemon=True)
update_thread.start()

def run():

    '''
    Edit this function only! (everything else is part of the update checker)
    '''

    try:

        from django.core.management import execute_from_command_line

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seng.server.settings")

        if len(sys.argv[1:]) and sys.argv[1] == 'migrate':
            execute_from_command_line(['main.py', 'migrate'])
        else:
            execute_from_command_line(['main.py', 'runserver', '127.0.0.1:5002'])

    finally:

        EXIT_QUEUE.put('exit')

main_thread = threading.Thread(name='Main Thread', target=run, daemon=True)
main_thread.start()

EXIT_QUEUE.get() # block until we get a QUIT status
time.sleep(1)
