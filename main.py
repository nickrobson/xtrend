#!/usr/bin/env python3

'''
DO NOT REMOVE THIS FILE

It is used as the entry point for the project.

Don't edit the next bit of code as it's the update checker.
'''

import json
import os.path
import threading
import time

VERSION_FILE = '.version'

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
        print('Getting current version')
        new_hash = check_update()
        if new_hash != current_version:
            current_version = new_hash
            print('Found new version -- restarting!')
            sys.exit(0)
        time.sleep(20) # sleep and check 20 seconds later!

thread = threading.Thread(name='Update Checker', target=thread_main, daemon=True)
thread.start()

'''
Edit from here onwards! (above is the update checker)
'''

import example

example.run() # for now, just execute the example