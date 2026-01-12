#!/usr/bin/env python3
"""
Ticinese Language Encyclopedia Launcher
Starts a local web server and opens the encyclopedia in the default browser
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import time
from threading import Thread

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 8080

class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler that doesn't print every request"""
    def log_message(self, format, *args):
        pass  # Suppress console output

def start_server():
    """Start the HTTP server"""
    os.chdir(SCRIPT_DIR)

    with socketserver.TCPServer(("", PORT), QuietHTTPRequestHandler) as httpd:
        print(f"Ticinese Encyclopedia is running...")
        print(f"Server started on http://localhost:{PORT}")
        print("\nYou can close this window when you're done using the encyclopedia.")
        print("The browser window will open automatically in a few seconds...\n")
        httpd.serve_forever()

def open_browser():
    """Wait a moment then open the browser"""
    time.sleep(2)
    webbrowser.open(f'http://localhost:{PORT}/index.html')

if __name__ == '__main__':
    # Start browser opener in separate thread
    browser_thread = Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    # Start server (blocking)
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n\nEncyclopedia closed. Thank you for using the Ticinese Encyclopedia!")
        sys.exit(0)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\nPort {PORT} is already in use. The encyclopedia may already be running.")
            print("Check if you have another browser window open with the encyclopedia.")
            input("\nPress Enter to exit...")
        else:
            raise
