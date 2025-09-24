#!/usr/bin/env python3
"""
Startup script to run both the ROMA service and main FastAPI application
"""
import subprocess
import sys
import time
import threading
import os

def run_roma_service():
    """Run the ROMA service in the background"""
    print("Starting ROMA service on port 3001...")
    subprocess.run([sys.executable, "roma_service.py"], check=False)

def run_main_app():
    """Run the main FastAPI application"""
    print("Starting main FastAPI application on port 5000...")
    subprocess.run([sys.executable, "main.py"], check=False)

if __name__ == "__main__":
    # Start ROMA service in a separate thread
    roma_thread = threading.Thread(target=run_roma_service, daemon=True)
    roma_thread.start()
    
    # Give ROMA service a moment to start
    time.sleep(2)
    
    # Start main application
    run_main_app()