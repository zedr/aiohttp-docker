import os
from datetime import datetime

from aiohttp import web


HOSTNAME = os.environ.get("HOSTNAME")


async def hello(request):
    timestamp = datetime.now().isoformat()
    return web.Response(text=f"{HOSTNAME} received at {timestamp}")


def main():
    web_app = web.Application()
    web_app.router.add_get("/", hello)
    web.run_app(web_app)


if __name__ == "__main__":
    main()

