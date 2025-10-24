import pandas as pd
import os
import requests
from pathlib import Path
import sqlalchemy
import numpy as np
from time import time
import math

# Own libs
from config import config


class Config:
    def __init__(self, config: dict) -> None:
        for key, value in config.items():
            setattr(self, key, value)


class PipelineRun(Config):
    def get_file(self, file_name: str) -> None:
        url = self.url
        file_url = url + "/" + file_name

        response = requests.get(file_url)

        with open(f"{file_name}", "wb") as file:
            file.write(response.content)

    def file_to_df(self, file_name: str) -> pd.DataFrame:
        file_extension = file_name.split(".")[-1]
        if file_extension == "csv":
            return pd.read_csv(file_name)
        elif file_extension == "parquet":
            return pd.read_parquet(file_name)
        else:
            raise Exception(f"File not supported: {file_extension}")

    def dfcolumn_to_datetime(self, df: pd.DataFrame, column_name: str) -> pd.DataFrame:
        df[f"{column_name}"] = pd.to_datetime(df[f"{column_name}"])
        return df

    def _create_sql_engine(self):
        engine = ""
        return engine

    def df_to_sql(self, df: pd.DataFrame, table_name: str) -> None:
        engine = self._create_sql_engine()
        chunks = int(math.ceil((len(df) / 1000)))
        df_iter = np.array_split(df, chunks)

        df_first_chunk = next(df_iter)
        df.head().to_sql(table_name, engine, if_exists="replace")
        df_first_chunk.to_sql(table_name, engine, if_exists="append")
        for chunk in df_iter:
            chunk.to_sql(table_name, engine, if_exists="append")
