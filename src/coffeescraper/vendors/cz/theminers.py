from vendors.vendors_abstract import *


class _TheMiners(VendorBase, ABC):
    def product_list(self, soup):
        return soup.find_all("li", {"data-hook": "product-list-grid-item"})

    @property
    def base_url(self):
        return "https://www.theminers.eu/"

    def name(self, list_item):
        return list_item.find("h3").text.strip()

    def _eshop_url_getter(self, list_item):
        return list_item.a.attrs["href"].strip() + "?lang=cs"

    def _price_getter(self, list_item) -> str:
        return list_item.find("span", {"data-hook": "product-item-price-to-pay"}).text

    def _price_range(self, price_list, **kwargs) -> int:
        q = 250  # default prices listed for 250g
        return super()._price_range(price_list[0]/q)

    def photo_url(self, list_item):
        tmp = list_item.find("div", {"data-hook": "product-item-images"}).attrs["style"]
        tmp = tmp[tmp.index("(")+1: tmp.index(")")]
        return tmp

    @scrape_from_product_detail
    def _keywords_getter(self, list_item):
        try:
            return list_item.select("pre > p")[0].text.strip().split(", ")
        except IndexError:
            return []

    @scrape_from_product_detail
    def about(self, list_item):
        return list_item.find_all("div", {"data-hook": "info-section-description"})[-1].text.strip()


class TheMinersFilter(_TheMiners):
    @property
    def download_url(self):
        return "https://www.theminers.eu/eshop?lang=cs&Typ+produktu=Pražené+na+filtr"


class TheMinersEspresso(_TheMiners):
    @property
    def download_url(self):
        return "https://www.theminers.eu/eshop?lang=cs&Typ+produktu=Pražené+na+espresso+"