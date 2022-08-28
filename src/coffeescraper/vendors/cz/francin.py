from vendors.vendors_abstract import *


class _Francin(VendorBase, ABC):
    def product_list(self, soup):
        return soup.select(".product")

    @property
    def base_url(self):
        return "https://www.francin.cz/"

    def name(self, list_item):
        return list_item.find("h2", "woocommerce-loop-product__title").contents[0].strip()

    def _eshop_url_getter(self, list_item):
        return list_item.a.attrs['href']

    def _price_getter(self, list_item) -> str:
        return list_item.find("bdi").text

    def photo_url(self, list_item):
        return list_item.img.attrs['data-src']

    def _price_range(self, price_list, **kwargs) -> int:
        """
        Francin has prices for 250g --> kc/g == price_list[0] / 250
        :param **kwargs:
        :param price_list:
        :return:
        """
        return super()._price_range(price_list[0]/250)

    def _keywords_getter(self, list_item):
        return list(map(str.strip, list_item.find("div", "taste-profile").contents[0].split(",")))

    def roast_level(self, list_item):
        return " ".join(list_item.find("div", "typPrazeni").text.split())

    @scrape_from_product_detail
    def about(self, list_item):
        return list_item.select("div .col-md-8, .col-md-push-2")[0].text.strip()


class FrancinFilter(_Francin):
    @property
    def download_url(self):
        return "https://www.francin.cz/vyberova-kava/filtr/"


class FrancinEspresso(_Francin):
    @property
    def download_url(self):
        return "https://www.francin.cz/vyberova-kava/espresso/"