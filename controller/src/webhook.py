import json
import logging
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, ParseResult

from validator import Validator

LOGGER = logging.getLogger(__name__)


class Controller(BaseHTTPRequestHandler):

    def do_POST(self):
        payload: dict = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        LOGGER.info("Processing request")
        response = self.process_request(payload, self.path)
        if response:
            self.send_response(200)
        else:
            self.send_response(404)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))

    @staticmethod
    def process_request(payload: dict, path: str) -> str:
        parse_result: ParseResult = urlparse(path)
        if parse_result.path == '/validate':
            LOGGER.info("...validating")
            return Validator.validate(payload)
        LOGGER.error("Path '%s' is incorrect, should be '/validate'", parse_result.path)
        return ""
