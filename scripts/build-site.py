#!/usr/bin/env python3
"""
Build site for testing
"""

import subprocess
import sys

def build_site(production=False):
    """Build Pelican site"""
    config = "publishconf.py" if production else "pelicanconf.py"
    mode = "production" if production else "development"
    
    print(f"Building site in {mode} mode...")
    
    try:
        result = subprocess.run([
            "pelican", "content", "-s", config
        ], check=True, capture_output=True, text=True)
        
        print("Build completed successfully!")
        print(f"Output directory: ./output/")
        
        if production:
            print("Site ready for deployment")
        else:
            print("Run 'python scripts/dev-server.py' to preview")
            
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    production = "--production" in sys.argv
    build_site(production)