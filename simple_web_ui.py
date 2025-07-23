#!/usr/bin/env python3
"""
Simple Web UI server for GenAI Pipeline
"""

import http.server
import socketserver
import webbrowser
import os
import argparse

def start_server(port=8000):
    """Start HTTP server for web UI"""
    # Change to the web_ui directory
    web_ui_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_ui")
    os.chdir(web_ui_dir)
    
    # Rename simple.html to index.html temporarily
    if os.path.exists("simple.html") and not os.path.exists("index.html.bak"):
        if os.path.exists("index.html"):
            os.rename("index.html", "index.html.bak")
        os.rename("simple.html", "index.html")
    
    # Create handler
    handler = http.server.SimpleHTTPRequestHandler
    
    # Create server
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Server started at http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        
        # Open browser
        webbrowser.open(f"http://localhost:{port}")
        
        # Serve until interrupted
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start Web UI server for GenAI Pipeline')
    parser.add_argument('--port', '-p', type=int, default=8000, help='Port to listen on')
    
    args = parser.parse_args()
    
    start_server(args.port)