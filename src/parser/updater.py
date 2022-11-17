from datetime import datetime
from parser.download import Downloader

import pandas as pd
from loguru import logger
from sqlmodel import Session
from tqdm import tqdm

import dependencies
from internal.crud import crud
from store.models import Category, PriceRecord, Product


class Updater:
    def __init__(self) -> None:
        self.downloader = Downloader()
        self.df = pd.DataFrame()
        self.session = Session(dependencies.engine)

    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        df.drop_duplicates(subset=["article"], inplace=True)
        df.reset_index(drop=True, inplace=True)
        df["article"] = df["article"].astype("int64")
        df["price"] = df["price"].apply(lambda x: x.replace(" ", ""))
        df["price"] = df["price"].astype("int64")
        return df

    def update_store(self) -> pd.DataFrame:
        categories = self.downloader.categories()

        for category in tqdm(categories):
            try:
                tmp_df = pd.DataFrame(self.downloader.products(category))
                self.df = pd.concat([self.df, tmp_df])
            except Exception as e:
                logger.error(f"{e}, on {category}")
                continue

        self.df = self.clean_dataframe(self.df)
        return self.df

    def upload_to_db(self, dataset: pd.DataFrame) -> None:
        with self.session:
            for i, row in dataset.iterrows():
                category = crud.get_or_create(self.session, Category, name=row.category)
                product = crud.get_or_create(
                    self.session,
                    Product,
                    article=row.article,
                    name=row.title,
                    category=category.id,
                    price=row.price,
                )
                product.updated_at = datetime.now()
                product.price = row.price
                crud.save(self.session, product)
                crud.create_object(self.session, PriceRecord, price=row.price, product=product.id)
        logger.info(f"Store updated on {len(dataset)} products")

    def run(self) -> None:
        self.update_store()
        self.upload_to_db(self.df)
