import os
import sys
import signal
import asyncio
import logging
from datetime import datetime
from concurrent.futures import CancelledError

from aiohttp import web


HOSTNAME = os.environ.get("HOSTNAME")
DEFAULT_LOGFILEPATH = "/var/log/aiohttp-demo.log"
LOGFILEPATH = os.environ.get("LOGFILEPATH", DEFAULT_LOGFILEPATH)

logger = logging.getLogger(__name__)
_fh = logging.FileHandler(LOGFILEPATH)
_fh.setLevel(logging.DEBUG)
logger.addHandler(_fh)


def handle_sighup():
    logger.warn("Received SIGHUP")
    for task in asyncio.Task.all_tasks():
        task.cancel()


async def hello(request):
    timestamp = datetime.now().isoformat()
    return web.Response(text=f"{HOSTNAME} received at {timestamp}")


async def health(request):
    return web.Response(text="HEALTHY")


def main():
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGHUP, handle_sighup)
    web_app = web.Application(loop=loop)
    web_app.router.add_get("/", hello)
    web_app.router.add_get("/health", health)
    try:
        web.run_app(web_app)
    except CancelledError:
        loop.close()


if __name__ == "__main__":
    main()

