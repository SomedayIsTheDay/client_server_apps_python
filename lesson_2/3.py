import yaml

data = {
    "list": ["2999€", "12€", "22222222€"],
    "number": "1€",
    "dict": {"first": "123123€", "second": "54545€", "third": "767676€"},
}

with open("data.yml", "w", encoding="utf-8") as f:
    yaml.dump(data, f, allow_unicode=True, default_flow_style=True)

with open("data.yml", "r", encoding="utf-8") as f:
    content = yaml.load(f, Loader=yaml.FullLoader)

print(content == data)
