#!/usr/bin/env python3
"""
Simple HTTP server to serve the web UI
"""

import http.server
import socketserver
import webbrowser
import os

# Define port
PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    """Start the server and open the web UI"""
    # Change to the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create the server
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Server started at http://localhost:{PORT}")
        print(f"Open your browser to http://localhost:{PORT}/simple_web_ui.html")
        print("Press Ctrl+C to stop the server")
        
        # Open the web UI in the default browser
        webbrowser.open(f"http://localhost:{PORT}/simple_web_ui.html")
        
        # Start the server
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == "__main__":
    main()