import requests
import smtplib
from email.mime.text import MIMEText
import time
import datetime
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)
user_interval = 3 #default

@app.route("/interval", methods=["POST"])
def set_user_interval():
    global user_interval
    data = request.json
    interval = data.get("interval")
    if interval is None or not type(interval) == int:
        return (jsonify({"error: interval not int"}), 400)
    
    user_interval = interval
    return (jsonify({"message": f"Interval set to {user_interval} seconds"}), 200)

urls = ["http://localhost:5173/", "https://google.com", "https://discord.com", "https://visuallearner.org", "https://claude.ai", "https://leetcode.com/problemset"]

previous_status = {url: (None, None) for url in urls} #bool, down_time

def check_url(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        latency = time.time() - start_time
        return (True, response.status_code,  latency)

    except requests.exceptions.Timeout:
        error = "Timeout"
    except requests.exceptions.ConnectionError:
        error = "Connection Failed"
    except requests.exceptions.RequestException:
        error = "Generic Error"
    
    return (False, str(error), None)

def false_positive_check(url, retries=2):
    for i in range(retries):
        result_tuple = check_url(url)
        (isWorking, status, latency) = result_tuple
        if isWorking:
            return (False, status, latency)

        time.sleep(2)
    
    return (True, status, latency)

def send_email(message, subject):
    sender = "hoaxsterburger@gmail.com"
    receiver = "jovanacarmel@gmail.com"
    app_password = "ehbr afwu jhat qhqb"

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, app_password)
            server.send_message(msg)
    except Exception as e:
        print(f"{e}")

def start():
    while True:
        print(f"entered loop in {user_interval} seconds\n")
        for url in urls:
            (isDown, status, latency) = false_positive_check(url)
            prev_state, timestamp = previous_status.get(url, None)

            if prev_state is None or prev_state != isDown: #if the previous value isnt the same as the current value, or its ur first time
                if isDown:
                    down_time_timestamp = datetime.datetime.now().replace(microsecond=0)

                    subject = "SERVER DOWN"
                    message = f"""
                        Service: {url}
                        Error: {status}
                        Time Stamp: {down_time_timestamp}"""
                    
                    previous_status[url] = (isDown, down_time_timestamp)

                else:
                    up_time_timestamp = datetime.datetime.now().replace(microsecond=0)
                    duration = up_time_timestamp - previous_status[url][1] if previous_status[url][1] is not None else datetime.timedelta(0)
                    
                    subject = "SERVER RESTORED"
                    message = f"""
                        Service: {url}
                        Status: {status} (WORKING)
                        Latency: {round(latency, 2)}s
                        Recovered Time: {up_time_timestamp}
                        Total Downtime: {duration.total_seconds()}s"""
                        
                    previous_status[url] = (isDown, None)
                
                if prev_state is not None: #only send when it is not first time 
                    send_email(message, subject)
            

        time.sleep(user_interval)

if __name__ == "__main__":
    start_thread = threading.Thread(target=start, daemon=True)
    start_thread.start()
    app.run(port=5000)