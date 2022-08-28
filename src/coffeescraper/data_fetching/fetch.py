import logging
import asyncio

import requests
from aiohttp import ClientSession, ClientResponseError, TCPConnector
from constants.network import HEADERS

logging.getLogger().setLevel(logging.DEBUG)


def fetch_text(url):
    x = requests.get(url, headers=HEADERS)
    if x.status_code == 200:
        return x.text
    raise Exception("Could not retrieve data from given url.")


async def fetch(session, url):
    try:
        async with session.get(url, timeout=15, headers=HEADERS) as response:
            resp = await response.text()
    except ClientResponseError as e:
        logging.warning(e)
    except asyncio.TimeoutError:
        logging.warning("Timeout")
    except Exception as e:
        logging.warning(e)
    else:
        logging.debug(f"Finished fetching for: {url}.")
        return resp
    return


async def fetch_async(loop, url: str, n_products: int = 1, page_size: int = 100):
    tasks = []
    # try to use one client session
    async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
        for offset in range(0, n_products, page_size):
            url_ = url.format(start=offset, page_size=page_size)
            task = asyncio.ensure_future(fetch(session, url_))
            tasks.append(task)
        # await response outside the for loop
        responses = await asyncio.gather(*tasks)
    return responses