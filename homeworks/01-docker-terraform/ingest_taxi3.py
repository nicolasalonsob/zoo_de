import pandas as pd
from pydantic import BaseModel


class Config(BaseModel):
    url: str
