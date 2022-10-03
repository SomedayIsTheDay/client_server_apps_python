from chardet import detect

with open("test.txt", "w", encoding="utf-8") as f:
    f.write("«сетевое программирование»,\n«сокет»,\n«декоратор».")

with open("test.txt", "rb") as f:
    content = f.read()
encoding = detect(content)["encoding"]

with open("test.txt", encoding=encoding) as f:
    for f_str in f:
        print(f_str, end="")
