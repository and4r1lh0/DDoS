import sys
import time
import random
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

class DefaultHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        
        n = random.randint(0,256)
        self.wfile.write((("{} is " + ("" if is_prime(n) else "not ") + "a prime number").format(n)).encode("utf-8"))

def base_http_server_start(address="0.0.0.0", port=8080):
    handler = DefaultHTTPHandler
    address = (address, port)
    server = ThreadingHTTPServer(address, handler, bind_and_activate=False)
    server.server_bind()
    server.server_activate()
    server.serve_forever()

def is_prime(num):
    res = True
    for i in range(2, num - 1):
        if num % i == 0:
            res = False
    return res

if __name__ == '__main__':
    print("Starting HTTP server on port 8080")
    base_http_server_start()
