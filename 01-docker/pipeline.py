import pandas as pd
import yaml
import os
import argparse
from pathlib import Path
from loguru import logger
from sqlalchemy import create_engine
from time import time


def create_config(pwd: str, file_name: str) -> dict:
    config_path = Path(pwd, "config", file_name)
    logger.info("Reading config file")
    with open(config_path, "r") as file:
        config_dict = yaml.safe_load(file)
    logger.info("Config file loaded")
    return config_dict


def create_sql_engine(params):
    dialect = params.dialect
    user = params.user
    psw = params.psw
    host = params.host
    port = params.port
    db = params.db

    engine = create_engine(f"{dialect}://{user}:{psw}@{host}:{port}/{db}")
    return engine


def transform_chunk(df):
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    return df


def run(config, params):
    sql_engine = create_sql_engine(params)
    chunk_size = 100000
    table_name = params.table_name
    csv_path = config["path"]["csv_data"]

    logger.info("Starting CSV ingestion...")

    # Create iterator
    df_iter = pd.read_csv(csv_path, iterator=True, chunksize=chunk_size)

    # Initialize table schema with first chunk
    first_chunk = transform_chunk(next(df_iter))
    first_chunk.head(0).to_sql(
        name=table_name, con=sql_engine, if_exists="replace", index=False
    )

    chunk_counter = 0
    t_start = time()
    first_chunk.to_sql(name=table_name, con=sql_engine, if_exists="append", index=False)
    t_end = time()
    chunk_counter += 1
    logger.info(
        f"Chunk number:{chunk_counter} inserted in t:{(t_end - t_start)} second"
    )

    for chunk in df_iter:
        chunk_counter += 1
        t_start = time()
        chunk = transform_chunk(chunk)
        chunk.to_sql(name=table_name, con=sql_engine, if_exists="append", index=False)
        t_end = time()
        logger.info(
            f"Chunk number:{chunk_counter} inserted in t:{(t_end - t_start)} second"
        )

    logger.info("CSV ingestion completed successfully.")


if __name__ == "__main__":
    pwd = os.getcwd()
    CONFIG_FILE_NAME = "config.yml"
    config = create_config(pwd, CONFIG_FILE_NAME)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--dialect", required=True)
    arg_parser.add_argument("--user", required=True)
    arg_parser.add_argument("--psw", required=True)
    arg_parser.add_argument("--host", required=True)
    arg_parser.add_argument("--port", required=True)
    arg_parser.add_argument("--db", required=True)
    arg_parser.add_argument("--table_name", required=True)
    args = arg_parser.parse_args()

    run(config, args)
