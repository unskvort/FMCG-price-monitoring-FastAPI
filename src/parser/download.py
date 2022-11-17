import time
from typing import Any, List, Type

import requests
from bs4 import BeautifulSoup
from latest_user_agents import get_random_user_agent
from loguru import logger


class Downloader:
    def __init__(self) -> None:
        self.BASE_URL = "https://myspar.ru"
        self.POSTFIX = "?sort=rating"
        self.HEADERS = {"User-Agent": get_random_user_agent()}

    def _download(
        self,
        path: str | None = None,
        timeout: int = 10,
        requests_interval: int = 10,
        max_requests_number: int = 1,
    ) -> bytes | None:
        url = self.BASE_URL + path + self.POSTFIX  # type: ignore
        for num_query in range(max_requests_number):
            try:
                request = requests.get(url, headers=self.HEADERS, timeout=timeout)
                if request.headers.get("content-type") == "text/html; charset=UTF-8":
                    return request.content
            except Exception as e:
                logger.error(f"{e}")
                logger.info(f"A second request to the {url} will be sent in {requests_interval} seconds")
                time.sleep(requests_interval)
                continue
        return None

    def categories(self) -> Type[List[Any]]:
        categories: list[str] = []
        request = self._download(path="/catalog/")
        if request:
            soup = BeautifulSoup(request, "html.parser")
            links = soup.find_all(class_="section-tile__link")
            for link in links:
                categories.append(link.find(class_="js-cut-text").get("href"))
        return categories  # type: ignore

    def products(self, category: str) -> dict[str, list[str]]:
        request = self._download(path=category)
        soup = BeautifulSoup(request, "html.parser")
        dataset: dict[str, list[str]] = {"title": [], "article": [], "price": []}
        category_product = soup.find("meta", attrs={"name": "keywords"}).get("content")
        products = soup.find_all(class_="catalog-list__item js-list-paging-item col-md-6 col-xl-4")

        for product in products:
            dataset["title"].append(product.find(class_="catalog-tile__name js-cut-text").text)
            dataset["article"].append(
                product.find(class_="catalog-tile__favorite js-favorite").get("data-item-article")
            )
            dataset["price"].append(product.find(class_="prices__cur js-item-price").text[:-4])
        dataset["category"] = [category_product] * len(dataset["title"])
        return dataset
