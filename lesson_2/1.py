import csv
import re
from chardet import detect


def get_data(*args):
    main_data = [["Изготовитель ОС", "Название ОС", "Код продукта", "Тип системы"]]
    for file in args:
        os_manufacturers, os_names, prod_codes, os_types = [], [], [], []

        with open(file, "rb") as f:
            content = f.read()
            encoding = detect(content)["encoding"]
            content = content.decode(encoding).encode("utf-8").decode("utf-8")
            info = re.findall(
                r"(Изготовитель ОС|Название ОС|Код продукта|Тип системы):\s+(.+[^\r\n ])",
                content,
            )
            for i, v in info:
                if i == "Название ОС":
                    os_names.append(v)
                elif i == "Изготовитель ОС":
                    os_manufacturers.append(v)
                elif i == "Код продукта":
                    prod_codes.append(v)
                else:
                    os_types.append(v)
        main_data.extend([os_manufacturers + os_names + prod_codes + os_types])
    print(main_data)
    return main_data


def write_to_csv(filename):
    data = get_data(
        "info_1.txt",
        "info_2.txt",
        "info_3.txt",
    )

    with open(filename + ".csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)


write_to_csv("data")
