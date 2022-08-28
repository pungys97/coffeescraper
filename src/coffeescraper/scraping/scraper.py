import itertools
import time
import unicodedata

from bs4 import BeautifulSoup
import logging
import asyncio

from icecream import ic

from vendors.vendors_abstract import VendorBase
from data_fetching.fetch import fetch_async

logging.getLogger().setLevel(logging.DEBUG)


def content_scraper(fetched_text, vendor: VendorBase) -> list:
    soup = BeautifulSoup(fetched_text, 'html.parser')
    ret = []
    for idx, product in enumerate(vendor.product_list(soup)):
        name = idx  # if name extraction fails we get index of the product
        try:
            eshop_url = vendor.eshop_url(product) # should always be run first to set _url_to_current_product
            brewing_method = vendor.brewing_methods(product)
            if not brewing_method: # empty --> not a coffee product
                continue
            name = vendor.name(product)
            for skip_name in VendorBase._skip_these_names:
                assert skip_name not in name.lower(), f"Name contains - {skip_name}"
            photo_url = vendor.photo_url(product)
            price, price_range = vendor.price(product)
            roast_level = vendor.roast_level(product)
            keywords = vendor.keywords(product)  # needs to run before calling acidity or bitterness
            acidity = vendor.acidity
            bitterness = vendor.bitterness
            sweetness = vendor.sweetness
            about = vendor.about(product)
        except AttributeError as e:  # do not want to upload incomplete data
            logging.warning(f"Product {name} failed during extraction from {vendor.download_url}. Reason - {e}.")
            continue
        except AssertionError as e:
            logging.info(f"Skipping - {e}")
            continue
        except Exception as e:
            logging.info(f"Error - {e}")
            continue

        ret.append({
            "name": name,
            "eshop_url": eshop_url,
            "photo_url": photo_url,
            "price": price,
            "price_range": price_range,
            "roast_level": roast_level,
            "acidity": acidity,
            "bitterness": bitterness,
            "sweetness": sweetness,
            "keywords": keywords,
            "brewing_method": brewing_method,
            "about": unicodedata.normalize("NFKD", about)
        })
    return ret


class Scraper:
    def __init__(self, vendors: list[VendorBase]):
        self.vendors = vendors
        assert vendors is not None, "Vendor must not be None."
        logging.debug(f"Scraper for {vendors} __init__ finished.")

    def _debug(self):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(fetch_async(loop, self.vendors[0].download_url))
        loop.run_until_complete(future)
        responses = future.result()
        soup = BeautifulSoup(responses[0], 'html.parser')
        return soup

    def scrape_one(self, vendor: VendorBase):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(fetch_async(loop, vendor.download_url))
        loop.run_until_complete(future)
        responses = future.result()
        data = list(itertools.chain(*map(lambda fetched_text: content_scraper(fetched_text, vendor), responses)))
        return data

    def scrape(self):
        start_time = time.time()
        data = []
        for vendor in self.vendors:
            data.extend(self.scrape_one(vendor))
        logging.info('Fetch %s products takes %s seconds', len(data), str(time.time() - start_time))
        return data
