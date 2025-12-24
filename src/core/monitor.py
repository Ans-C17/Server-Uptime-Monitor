import time, requests
from src.core.config import DELAY, TIMEOUT

def check_url(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=TIMEOUT)
        latency = time.time() - start_time
        return (True, response.status_code,  latency)

    except requests.exceptions.Timeout:
        error = "Timeout"
    except requests.exceptions.ConnectionError:
        error = "Connection Failed"
    except requests.exceptions.RequestException:
        error = "Generic Error"
    
    return (False, str(error), None)

def false_positive_check(url, retries):
    for i in range(retries):
        result_tuple = check_url(url)
        (isWorking, status, latency) = result_tuple
        if isWorking:
            return (False, status, latency)

        time.sleep(DELAY)
    
    return (True, status, latency)