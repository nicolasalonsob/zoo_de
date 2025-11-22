"""
1. Get the file (do i want the file in local? or put just buffer it? maybe in local looks like more prod code, like "datalake")
2. Change the datetime
3. Ingest it into sql
4. Module the code
"""

import requests
from pydantic import BaseModel
from pathlib import Path
from loguru import logger
import yaml


class Config(BaseModel):
    url: str
    file_name: str
    file_dir: str


def yaml_to_dict(yaml_file_path: str | Path) -> dict:
    with open(yaml_file_path, "r") as file:
        return yaml.safe_load(file)


def get_file(url: str, file_name: str, destination_path: str) -> None:
    file_url = f"{url}/{file_name}"

    try:
        logger.info(f"Fetching file {file_url}")
        response = requests.get(file_url)
        response.raise_for_status()
        logger.info("Success downloading file!")
        file_path = Path(destination_path, file_name)
        with open(file_path, "wb") as file:
            file.write(response.content)
        logger.info(f"Success {file_path} writing the file")

    except requests.exceptions.HTTPError as e:
        logger.error(
            f"HTTP Error fetching the file \n Satus:{response.status_code} \n Error: {e}"
        )

    except IOError as e:
        logger.error(f"IO Error writeing the file: {e}")

    except Exception as e:
        logger.error(f"Unexpectede error fetching/writing file: {e}")
        raise
