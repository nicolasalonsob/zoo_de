# pipeline.py
import math
import numpy as np
import pandas as pd
import requests
from pathlib import Path
from sqlalchemy import create_engine
from pydantic import BaseModel, HttpUrl


# -------------------
# Configuration
# -------------------
class PipelineConfig(BaseModel):
    url: HttpUrl
    chunk_size: int = 1000
    db_connection_string: str


# -------------------
# File Utilities
# -------------------
def download_file(url: str, file_name: str) -> None:
    file_url = f"{url}/{file_name}"
    response = requests.get(file_url)
    response.raise_for_status()  # fail if request fails
    Path(file_name).write_bytes(response.content)  # write in binary mode


def file_to_df(file_name: str) -> pd.DataFrame:
    file_extension = file_name.split(".")[-1].lower()
    if file_extension == "csv":
        return pd.read_csv(file_name)
    elif file_extension == "parquet":
        return pd.read_parquet(file_name)
    else:
        raise ValueError(f"File not supported: {file_extension}")


# -------------------
# DataFrame Utilities
# -------------------
def convert_column_to_datetime(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    df[column_name] = pd.to_datetime(df[column_name])
    return df


# -------------------
# Database Utilities
# -------------------
class SQLWriter:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)

    def write_df(
        self, df: pd.DataFrame, table_name: str, chunk_size: int = 1000
    ) -> None:
        if df.empty:
            return

        n_chunks = max(1, math.ceil(len(df) / chunk_size))
        df_iter = np.array_split(df, n_chunks)

        # first chunk with replace
        first_chunk = next(iter(df_iter))
        first_chunk.to_sql(table_name, self.engine, if_exists="replace", index=False)

        # remaining chunks with append
        for chunk in df_iter:
            chunk.to_sql(table_name, self.engine, if_exists="append", index=False)


# -------------------
# Pipeline Orchestration
# -------------------
class PipelineRun:
    def __init__(self, config: PipelineConfig):
        self.config = config

    def run(self, file_name: str, table_name: str, datetime_columns: list[str] = []):
        # download
        download_file(self.config.url, file_name)

        # load to DataFrame
        df = file_to_df(file_name)

        # transform datetime columns
        for col in datetime_columns:
            df = convert_column_to_datetime(df, col)

        # write to SQL
        writer = SQLWriter(self.config.db_connection_string)
        writer.write_df(df, table_name, chunk_size=self.config.chunk_size)


# -------------------
# Example usage
# -------------------
if __name__ == "__main__":
    config = PipelineConfig(
        url="https://my-data-source.com",
        chunk_size=1000,
        db_connection_string="postgresql+psycopg2://user:pass@host:port/db",
    )

    pipeline = PipelineRun(config)
    pipeline.run(
        file_name="data.csv", table_name="my_table", datetime_columns=["date_col"]
    )
