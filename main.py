#!/usr/bin/env python3

'''
DO NOT REMOVE THIS FILE

It is used as the entry point for the project.

Don't edit the next bit of code as it's the update checker.
'''

import json
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
            EXIT_QUEUE.put('exit')
            break
        time.sleep(30) # sleep and check 30 seconds later!

update_thread = threading.Thread(name='Update Checker', target=thread_main, daemon=True)
update_thread.start()

'''
Edit from here onwards! (above is the update checker)
'''

def run():

    try:

        import example

        example.run() # for now, just execute the example

    except SystemExit:
        pass

    EXIT_QUEUE.put('exit')

main_thread = threading.Thread(name='Main Thread', target=run, daemon=True)
main_thread.start()

EXIT_QUEUE.get() # block until we get a QUIT status
