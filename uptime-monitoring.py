import requests
import time
import logging

# URLs to monitor
urls = [
    "http://www.example.com/nonexistentpage",
    "http://httpstat.us/404",
    "http://httpstat.us/500",
    "https://www.google.com/"
]

# Logging configuration
logging.basicConfig(
    filename="uptime_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Track error counts for exponential backoff
error_count = {url: 0 for url in urls}

check_interval = 10

while True:

    for url in urls:

        try:
            print("\nChecking URL:", url)

            response = requests.get(url)

            status_code = response.status_code
            status_text = response.reason

            print(f"Status Code: {status_code} {status_text}")

            logging.info(f"{url} - {status_code} {status_text}")

            if 400 <= status_code < 500:
                print(f"ALERT: 4xx error encountered for URL: {url}")
                logging.warning(f"4xx error detected for {url}")
                error_count[url] += 1

            elif 500 <= status_code < 600:
                print(f"ALERT: 5xx error encountered for URL: {url}")
                logging.warning(f"5xx error detected for {url}")
                error_count[url] += 1

            else:
                print("The website is UP and running.")
                error_count[url] = 0

        except requests.exceptions.RequestException as e:
            print("Connection Error:", e)
            logging.error(f"Connection error for {url} : {e}")
            error_count[url] += 1

        if error_count[url] > 0:
            backoff_time = check_interval * (2 ** error_count[url])
            print(f"Retrying after {backoff_time} seconds due to repeated errors...")
            time.sleep(backoff_time)

    print("\nWaiting before next monitoring cycle...\n")
    time.sleep(check_interval)