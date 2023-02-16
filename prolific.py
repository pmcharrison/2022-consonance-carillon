import json

from dallinger.config import get_config
from dallinger.prolific import ProlificService


config = get_config()
config.load()

service = ProlificService(
    api_token=config.get("prolific_api_token"),
    api_version=config.get("prolific_api_version"),
    referer_header=f"https://github.com/Dallinger/Dallinger/v9.4.1",
)

study = service.get_study("63ee544ee74b60edd5235863")
print(json.dumps(study, indent=4))
