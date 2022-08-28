import inspect
import json

import vendors.cz
from scraping.scraper import Scraper


if __name__ == '__main__':
    s = Scraper([roaster[1]() for roaster in inspect.getmembers(vendors.cz, inspect.isclass)])
    data = s.scrape()
    with open("test/out.json", "w") as fp:
        json.dump(data, fp)
