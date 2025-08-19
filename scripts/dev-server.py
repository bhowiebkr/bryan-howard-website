#!/usr/bin/env python3
"""
Start development server with auto-reload
"""

import subprocess
import sys
import os

def start_dev_server():
    """Start Pelican development server"""
    print("Starting Pelican development server...")
    print("Site will be available at: http://localhost:8000")
    print("Press Ctrl+C to stop")
    
    try:
        # Start server with auto-reload
        subprocess.run([
            "pelican", "--listen", "--autoreload",
            "--bind", "127.0.0.1",
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\nDevelopment server stopped")
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_dev_server()