#!/usr/bin/env python3
"""
Simple HTTP server for GenAI Pipeline Web UI
"""

import http.server
import socketserver
import webbrowser
import os
import argparse

def start_server(port=8000):
    """Start HTTP server for web UI"""
    # Change to the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
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
    parser = argparse.ArgumentParser(description='Start HTTP server for GenAI Pipeline Web UI')
    parser.add_argument('--port', '-p', type=int, default=8000, help='Port to listen on')
    
    args = parser.parse_args()
    
    start_server(args.port)