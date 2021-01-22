#!/usr/bin/env python
"""
This example demonstrates how a single Counter metric collector can be created
and exposed via a HTTP endpoint.
"""
import asyncio
import socket
from contextlib import contextmanager
import random
from aioprometheus import Gauge, Service

if __name__ == "__main__":

    async def main(svr: Service) -> None:

        events_gauge = Gauge(
            "events_gauge", "Number of events.", const_labels={"host": socket.gethostname()}
        )
        svr.register(events_gauge)
        await svr.start(addr="localhost", port=5000)
        print(f"Serving prometheus metrics on: {svr.metrics_url}")

        @contextmanager
        def gouge_process_1():
            events_gauge.inc({"kind": "process_1"})
            yield
            events_gauge.dec({"kind": "process_1"})

        @contextmanager
        def gouge_process_2():
            events_gauge.inc({"kind": "process_2"})
            try:
                yield
            finally:
                events_gauge.dec({"kind": "process_2"})

        async def process(g: Gauge):
            while True:
                try:
                    with gouge_process_2():
                        with gouge_process_1():
                            await asyncio.sleep(0.5)
                            if random.random() < 0.5:
                                raise Exception
                except:
                    pass

        await process(events_gauge)


    loop = asyncio.get_event_loop()
    svr = Service()
    try:
        loop.run_until_complete(main(svr))
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(svr.stop())
    loop.close()
