import time
from flask import Flask, request, jsonify
import threading
from dotenv import load_dotenv
import sqlite3
import datetime

from src.core.config import DB, DEFAULT_INTERVAL, URLS, RETRIES
from src.core.monitor import false_positive_check
from src.services.email import send_email
from src.services.database import create_connection, insert_value, get_previous_values
from src.services.convert_time import convert_time

load_dotenv()

user_interval = DEFAULT_INTERVAL
app = Flask(__name__)

@app.route("/interval", methods=["POST"])
def set_user_interval():
    global user_interval
    data = request.json
    interval = data.get("interval")
    if interval is None or not type(interval) == int:
        return (jsonify({"error": "interval not int"}), 400)
    
    user_interval = interval
    return (jsonify({"message": f"Interval set to {user_interval} seconds"}), 200)

def start():
    connection = sqlite3.connect(DB)
    create_connection(connection)

    previous_status = get_previous_values(connection) #NOTE: stores isDown and down_time, NOT isUp, so true = down
    urls = URLS
    while True:
        print(f"entered loop in {user_interval} seconds\n")
        for url in urls:
            (isDown, status, latency) = false_positive_check(url, RETRIES)
            prev_state, prev_timestamp = previous_status.get(url, (None, None))
            print(f"PREVIOUS STATE: {url} -> {(prev_state, prev_timestamp)}\n")

            if prev_state is None or prev_state != isDown: #if the previous value isnt the same as the current value, or its ur first time
                if isDown:
                    down_time_timestamp = datetime.datetime.now().replace(microsecond=0)

                    subject = "SERVER DOWN"
                    message = f"""
                        Service: {url}
                        Error: {status}
                        Time Stamp: {down_time_timestamp}"""
                    
                    previous_status[url] = (True, down_time_timestamp)
                    insert_value(connection, url, status, None, down_time_timestamp.isoformat())

                else:
                    up_time_timestamp = datetime.datetime.now().replace(microsecond=0)
                    duration = up_time_timestamp - prev_timestamp if prev_timestamp is not None else datetime.timedelta(0)
                    
                    subject = "SERVER RESTORED"
                    message = f"""
                        Service: {url}
                        Status: {status} (WORKING)
                        Latency: {round(latency, 2)}s
                        Recovered Time: {up_time_timestamp}
                        Total Downtime: {convert_time(duration.total_seconds())}"""
                        
                    previous_status[url] = (False, None)
                    insert_value(connection, url, "WORKING", latency, up_time_timestamp.isoformat())
                
                if prev_state is not None: #only send when it is not first time 
                    send_email(message, subject)

        time.sleep(user_interval)

if __name__ == "__main__":
    start_thread = threading.Thread(target=start, daemon=True)
    start_thread.start()
    app.run(port=5000)