#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import threading
import json
import logging
from websocket_server import WebsocketServer

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s", level=logging.DEBUG)

class observer(threading.Thread):
    def __init__(self, value_name, host, port, interval=1):
        super(observer, self).__init__()
        self.interval = interval
        self.server = WebsocketServer(port,host)
        self.server.set_fn_new_client(self._on_new_client_appeared)
        self.server.set_fn_client_left(self._on_new_client_appeared)
        self.wsthread = threading.Thread(target=self.server.run_forever)
        self.value_name = value_name
    
    def _getvalue(self):
        pass

    def _on_new_client_appeared(self, client, server):
        logging.info("new client[{0}:{1}] appear here.".format(client["address"]))

    def _on_client_left(self, client, server):
        logging.info("client[{0}:{1}] has vanished.".format(client["address"]))

    def run(self):
        self.wsthread.start()
        try:
            while True:
                val = self._getvalue()
                if(val!=None):
                    data = {
                        "name": self.value_name,
                        "value": val
                    }
                    data_json = json.dumps(data)
                    self.server.send_message_to_all(data_json)
                    logging.debug(json.dumps(data, indent=2))
                time.sleep(self.interval)
        except KeyboardInterrupt as e:
            logging.info("Interrupted.")
        except Exception as e:
            logging.error(e)