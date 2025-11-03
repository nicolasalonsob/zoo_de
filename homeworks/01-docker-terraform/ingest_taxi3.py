from typing import Iterable
from pydantic import BaseModel
import requests
from loguru import logger
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy import Engine


class Config(BaseModel):
    file_name:str
    url:str
    provider:str
    postgres_user: str
    postgres_psw: str
    postgres_host: str
    postgres_db: str


def get_file(url: str, file_name: str) -> None:
    file_url = f"{url}/{file_name}"
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        Path(file_name).write_bytes(response.content)
        logger.info(f"File written {file_name}")
    except Exception as e:
        logger.error(f"Current write the file {file_name} with error: {e}")
        raise


def file_to_df_iter(file_name: str, chunk_size:int=100000) -> Iterable:
    readers = {
        ".csv": pd.read_csv,
        ".parqut": pd.read_parquet,
    }

    file_type = Path(file_name).suffix.lower()

    reader = readers.get(file_type)
    if not reader:
        logger.error(f"{file_type} not supported")

    try:
        logger.info(f"Converting {file_name} to df")
        return reader(file_name, iterator=True, chunk_size=chunk_size)
    except Exception as e:
        logger.error(f"file: {file_name} could not be converted to df with error {e}")
        raise


def column_to_datetime(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    try:
        logger.info(f"Converting column: {column_name} to datetime")
        df[column_name] = pd.to_datetime(df[column_name])
        return df
    except Exception as e:
        logger.error(f"Failed converting column:{column_name} with error: {e}")
        raise


class SqlEngine:
    def __init__(
        self, provider: str, host: str, port: int, db: str, user: str, psw: str
    ) -> None:
        self.provider = provider
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.psw = psw
        self.engine = None

    def connect(self) -> None:
        try:
            self.engine = create_engine(
                f"{self.provider}://{self.user}:{self.psw}@{self.host}:{self.port}/{self.db}"
            )
            logger.info("Sql engine created")

        except Exception as e:
            logger.error(f"Failed creating the sql conn with error: {e}")
            raise

    def df_to_sql(self, df: pd.DataFrame, table_name: str, mode: str) -> None:
        try:
            df.to_sql(name=table_name, con=self.engine, if_exists=mode, index=False)
            logger.info(f"{len(df)} rows inserted into table: {table_name}")
        except Exception as e:
            logger.error(f"Failed inserting df into {table_name} with error: {e}")

class Pipeline:
    def __init__(self, config:Config) -> None:
        self.config = config
        self.sql = SqlEngine(
            provider=config.provider, 
            host=config.host, 
            port=config.hots,
            db=config.db,
            user=config.user,
            psw=config.psw
        )
        self.sql.connect()
        self.tabl_name = config.file_name.split(".")[0]

    def run(self)-> None:

        get_file(url=self.config.url, file_name=self.config.file_name)

        df_iter = file_to_df_iter(self.config.file_name)

        for i in range(len(df_iter)):
                df = df_iter[i]
                df_transformed = column_to_datetime(df, )
                
            if i == 0:
                df_to_sql(df = df_iter[i], name = self.tabl_name, mode= "replace")
            else:
                df_to_sql(df = )
