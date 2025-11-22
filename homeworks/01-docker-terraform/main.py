from utils import utils
from pathlib import Path

yml_config_path = Path("config", "config.yml")

config_dict = utils.yaml_to_dict(yml_config_path)

config = utils.Config(**config_dict["files"])

print(config)

utils.get_file(config.url, config.file_name, config.file_dir)
