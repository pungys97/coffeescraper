from vendors.vendors_abstract import *


class _NordBeans(VendorBase, ABC):
    def product_list(self, soup):
        return soup.select(".product")

    @property
    def base_url(self):
        return "https://www.nordbeans.cz/"

    def name(self, list_item):
        parts = list_item.find("h3").contents
        parts.pop(1)  # remove <br>
        return " ".join(map(lambda x: x.text.capitalize(), parts))

    def _eshop_url_getter(self, list_item):
        return list_item.attrs['href']

    def _price_getter(self, list_item) -> str:
        return list_item.find("span", "price").text

    def _price_range(self, price_list, **kwargs) -> int:
        """
        Doubleshot is expensive --> classify all as expensive
        :param **kwargs:
        :param price_list:
        :return:
        """
        try:
            q = int(kwargs['list_item'].find("span", "quantity").text.strip().replace("g", ""))
        except AttributeError:
            q = 200 # default == 200g, could mess up price range but not currently important
        return super()._price_range(price_list[0]/q)

    def photo_url(self, list_item):
        return urllib.parse.urljoin(self.base_url, list_item.img.attrs['src'])

    @scrape_from_product_detail
    def _keywords_getter(self, list_item):
        tmp = list_item.find("span", {"class": "col-sm-8 col-xs-12"}).text.replace("–", "-")
        return tmp.split("-")

    @scrape_from_product_detail
    def about(self, list_item):
        return list_item.select("div .pad > p")[-1].text.strip()


class NordBeansFilter(_NordBeans):
    @property
    def download_url(self):
        return "https://www.nordbeans.cz/eshop/nordbeans/filtr/"


class NordBeansEspresso(_NordBeans):
    @property
    def download_url(self):
        return "https://www.nordbeans.cz/eshop/nordbeans/espresso/"