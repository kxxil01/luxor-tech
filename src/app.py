import urllib.request
import time
import threading
import schedule
import logging
from flask import Flask
from config import OTHER_SERVERS
import socket

app = Flask(__name__)

# Configure logging to include stdout output
logging.basicConfig(level=logging.INFO)

@app.route('/ping')
def ping_the_http_server():
    hostname = socket.gethostname()  # Get the hostname of the pod
    return f"Pong from {hostname}\n"

def ping_other_servers():
    for server in OTHER_SERVERS:
        try:
            response = urllib.request.urlopen(server['url'])
            if response.getcode() == 200:
                logging.info(f"Pinged {server['url']} - Response: {response.read().decode('utf-8').strip()}")
            else:
                logging.error(f"Failed to ping {server['url']} - Status Code: {response.getcode()}")
        except Exception as e:
            logging.error(f"Error while pinging {server['url']}: {e}")

def run_ping_schedule():
    schedule.every(60).seconds.do(ping_other_servers)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler loop in a separate thread
threading.Thread(target=run_ping_schedule).start()

if __name__ == "__main__":
    # Run Flask app
    app.run(host='0.0.0.0', port=5000)
