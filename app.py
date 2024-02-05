import threading
import time
import random
import json
import os
from datetime import datetime
from flask import Flask, jsonify

# Global counter
counter = 0

file_path = "counter.txt"
hour_production_path = "hour_production.txt"
total_production = 0 

lines_Details = [
    {   "line": 1,
        "count": 0,
        "maxCount": 12
    },
    {   "line": 2,
        "count": 0,
        "maxCount": 16
    },
    {
        "line": 3,
        "count": 0,
        "maxCount": 8
    }
]


# Function to read the last total production
def read_last_total_production():
    try:
        with open(hour_production_path, "r") as file:
            data = json.load(file)
            return data.get("totalProduction", 0)
    except FileNotFoundError:
        return 0
    except json.JSONDecodeError:
        return 0
    
# Function to reset the hour production
def reset_hour_production():
    with open(hour_production_path, "w") as file:
        file.write(json.dumps({"totalProduction": 0}))

def update_counter():
    total_production = read_last_total_production()

    while True:
        current_time = datetime.now()
        # Check if it's the first minute of an hour
        if current_time.minute == 38 and current_time.second == 0:
            reset_hour_production()
            total_production = 0

 # 6 times for 60 seconds
        time.sleep(60)
        for line_detail in lines_Details:
            increment = random.randint(0, line_detail["maxCount"])
            line_detail["count"] = increment
            total_production += increment

        # Write updated details to file
        with open(file_path, "w") as file:
            file.write(json.dumps(lines_Details))

        # Update hour_production file with new total production
        with open(hour_production_path, "w") as file:
            file.write(json.dumps({"totalProduction": total_production}))

        # Reset counts for each line
        for line_detail in lines_Details:
            line_detail["count"] = 0
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
    
@app.route('/get_hour_production', methods=['GET'])
def get_hour_production():
    try:
        with open(hour_production_path, "r") as file:
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