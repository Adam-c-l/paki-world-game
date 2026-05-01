#!/usr/bin/env python3
"""
Simple HTTP server for Render health checks.
This satisfies Render's HTTP port scanning while the lobby server runs.
"""

import http.server
import socketserver
import threading
import time

class HealthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK - Lobby Server Running')
    
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def start_http_server():
    """Start HTTP server on port 8080 for health checks"""
    with socketserver.TCPServer(("", 8080), HealthHandler) as httpd:
        print("HTTP health check server started on port 8080")
        httpd.serve_forever()

if __name__ == "__main__":
    start_http_server()
