import os
import sys
import signal
import asyncio
import logging
from datetime import datetime
from concurrent.futures import CancelledError

from aiohttp import web


HOSTNAME : str = os.environ.get("HOSTNAME", "Unknown")

_ns = {
    "count": 0
}


class AioHttpAppException(BaseException):
    """An exception specific to the AioHttp application."""


class GracefulExitException(AioHttpAppException):
    """Exception raised when an application exit is requested."""


class ResetException(AioHttpAppException):
    """Exception raised when an application reset is requested."""


def handle_sighup() -> None:
    logging.warning("Received SIGHUP")
    raise ResetException("Application reset requested via SIGHUP")


def handle_sigterm() -> None:
    logging.warning("Received SIGTERM")
    raise ResetException("Application exit requested via SIGTERM")


def cancel_tasks() -> None:
    for task in asyncio.Task.all_tasks():
        task.cancel()


async def hello(request: web.Request) -> web.Response:
    _ns['count'] += 1
    timestamp = datetime.now().isoformat()
    return web.Response(text=f"{HOSTNAME} received at {timestamp}")


async def health(request: web.Request) -> web.Response:
    return web.Response(text="HEALTHY")


async def metrics(request: web.Request) -> web.Response:
    return web.Response(
        text=(
            'http_requests_total'
            f'{{server="{HOSTNAME}"}} '
            f'{_ns["count"]}'
        )
    )


def run_app() -> bool:
    """Run the application

    Return whether the application should restart or not.
    """
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGHUP, handle_sighup)
    loop.add_signal_handler(signal.SIGTERM, handle_sigterm)

    web_app = web.Application()
    web_app.router.add_get("/", hello)
    web_app.router.add_get("/health", health)
    web_app.router.add_get("/metrics", metrics)

    try:
        web.run_app(web_app, handle_signals=True)
    except ResetException:
        logging.warning("Reloading...")
        cancel_tasks()
        asyncio.set_event_loop(asyncio.new_event_loop())
        return True
    except GracefulExitException:
        logging.warning("Exiting...")
        cancel_tasks()
        loop.close()

    return False


def main() -> None:
    """The main loop."""
    while run_app():
        pass


if __name__ == "__main__":
    main()

