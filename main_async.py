#!/usr/bin/env python
"""
This example demonstrates how a single Counter metric collector can be created
and exposed via a HTTP endpoint.
"""
import asyncio
import socket
from aioprometheus import Counter, Service


if __name__ == "__main__":

    async def main(svr: Service) -> None:

        events_counter = Counter(
            "events", "Number of events.", const_labels={"host": socket.gethostname()}
        )
        svr.register(events_counter)
        await svr.start(addr="", port=5000)
        print(f"Serving prometheus metrics on: {svr.metrics_url}")

        # Now start another coroutine to periodically update a metric to
        # simulate the application making some progress.
        async def updater(c: Counter):
            while True:
                c.inc({"kind": "timer_expiry"})
                await asyncio.sleep(1.0)

        await updater(events_counter)

    loop = asyncio.get_event_loop()
    svr = Service()
    try:
        loop.run_until_complete(main(svr))
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(svr.stop())
    loop.close()