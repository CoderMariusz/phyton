import threading
import time
import random
import json
import os
from flask import Flask, jsonify

# Global counter
counter = 0

file_path = "counter.txt"

# Function to update the counter and write to file
def update_counter():
    global counter
    while True:
        for _ in range(6):  # 6 times for 60 seconds
            time.sleep(10)
            counter += random.randint(0, 3)
        
            with open(file_path, "w") as file:
                file.write(json.dumps({"count": counter}))
        
        counter = 0

# Function to watch the file and print updates
def watch_file(file_path):
    last_modified = None
    while True:
        if os.path.exists(file_path):
            current_modified = os.path.getmtime(file_path)
            if current_modified != last_modified:
                with open(file_path, "r") as file:
                    data = file.read()
                    print(data)
                last_modified = current_modified
                # removed return statement to allow continuous monitoring
        time.sleep(1)


# Flask Web Server
app = Flask(__name__)

@app.route('/get_counter', methods=['GET'])
def get_counter():
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return jsonify(data)
    except Exception as e:
        return jsonify({"error": e})

# Start the counter and watcher threads
counter_thread = threading.Thread(target=update_counter)
watcher_thread = threading.Thread(target=watch_file)
counter_thread.start()
watcher_thread.start()

# Start Flask server (only if this script is the main program)
if __name__ == '__main__':
    app.run(debug=True)