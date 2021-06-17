import json


def parse_config(config, parameters):
    with open(config) as f:
        kwargs = json.load(f)
        for param in parameters:
            if not kwargs.get(param):
                kwargs[param] = None
        return kwargs
