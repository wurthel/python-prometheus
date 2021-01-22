import random
import time
from aioprometheus import Counter, Service

from prometheus_client import start_http_server, Summary, Counter

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing', 'Time spent processing request')
SUCCESS_COUNTER = Counter('request_success', 'Success request')
EXCEPTION_COUNTER = Counter('request_exception', 'Exceptions', ["name"])


# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    # Summarize time
    time.sleep(t)

    # Increase counter
    if random.random() < 0.5:
        SUCCESS_COUNTER.inc()

    # Increase exception
    if random.random() < 0.4:
        try:
            exception = random.choice([KeyError, KeyboardInterrupt, InterruptedError])
            with EXCEPTION_COUNTER.labels(name=repr(exception)).count_exceptions(exception):
                raise exception
        except:
            pass


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    port = 8000
    addr = ""
    start_http_server(port, addr=addr)
    # Generate some requests.
    while True:
        process_request(random.random())
