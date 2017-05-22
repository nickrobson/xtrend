from django.apps import AppConfig

class XNewsAppConfig(AppConfig):

    name = 'seng.server'
    verbose_name = 'SENG3011 Cool Bananas'

    def ready(self):

        import json
        import os
        import threading
        import time
        import _thread

        from ..core import logger
        from ..core.constants import RELEASE_VERSION

        logger.info('SENG3011 - Team Cool Bananas 2')
        logger.info('API 2: News')
        logger.info('Module version', RELEASE_VERSION)

        VERSION_FILE = '.version'

        if not os.path.exists(VERSION_FILE):
            return

        def run_update_thread():
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
                _thread.interrupt_main()


        update_thread = threading.Thread(name='Update Checker', target=run_update_thread, daemon=True)
        update_thread.start()

default_app_config = 'seng.server.XNewsAppConfig'