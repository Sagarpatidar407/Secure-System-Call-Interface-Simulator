import subprocess
import webbrowser
import time
import os
import sys
from dotenv import load_dotenv

def start_flask():
    # Load environment variables
    load_dotenv()
    
    print("Starting Flask server...")
    
    try:
        # Start Flask server in a separate process
        flask_process = subprocess.Popen(
            [sys.executable, 'run.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for the server to start
        print("Waiting for server to start...")
        time.sleep(3)
        
        # Check if the process is still running
        if flask_process.poll() is not None:
            print("Error: Flask server failed to start")
            stdout, stderr = flask_process.communicate()
            print("Error output:", stderr.decode())
            return
        
        # Open the browser
        print("Opening browser...")
        webbrowser.open('http://localhost:5000')
        
        print("Server is running. Press Ctrl+C to stop.")
        
        try:
            # Keep the script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping server...")
            flask_process.terminate()
            print("Server stopped.")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if 'flask_process' in locals():
            flask_process.terminate()

if __name__ == '__main__':
    start_flask() 