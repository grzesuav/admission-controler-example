import logging
import sys
import ssl
import threading
import time
from http.server import HTTPServer

from webhook import Controller


logging.basicConfig(stream=sys.stdout,  level="INFO")
LOGGER = logging.getLogger(__name__)


class ServerInThread(threading.Thread):
    def __init__(self, server: HTTPServer):
        super().__init__()
        self.server = server

    def run(self):
        LOGGER.info("Starting %s", self.server.RequestHandlerClass.__name__)
        self.server.serve_forever()


def main():
    LOGGER.info("Starting processor")

    httpd = HTTPServer(('', 4443), Controller)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   server_side=True,
                                   certfile='/certs/tls.crt',
                                   keyfile='/certs/tls.key',
                                   ca_certs='/certs/ca.crt',
                                   ssl_version=ssl.PROTOCOL_TLS)
    threads = [
        ServerInThread(httpd)
    ]
    for thread in threads:
        thread.start()

    while all(thread.is_alive() for thread in threads):
        # If any thread has died - restart
        time.sleep(1)

    raise Exception("Thread were killed")


if __name__ == "__main__":
    main()
