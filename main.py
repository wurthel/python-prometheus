from prometheus_client import start_http_server, Summary, Counter
import random
import time

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
SUCCESS_COUNTER = Counter('request_success_request', 'Success request')


# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)
    if random.random() > 0.5:
        SUCCESS_COUNTER.inc(1)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    port = 8000
    addr = ""
    start_http_server(port, addr=addr)
    # Generate some requests.
    while True:
        process_request(random.random())
