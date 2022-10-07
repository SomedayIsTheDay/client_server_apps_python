import json
from datetime import datetime


def write_order_to_json(item, quantity, price, buyer, date):
    with open("orders.json", "r", encoding="utf-8") as f:
        content = json.load(f)
    order = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date,
    }
    content["orders"].append(order)

    with open("orders.json", "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)


write_order_to_json("pillow", 23, 14444.00, "я", str(datetime.now()))
