strings = ["разработка", "администрирование", "protocol", "standard"]

for v in strings:
    print(v, type(v))
    b_str = v.encode(encoding="utf-8")
    print(b_str, type(b_str))
    v = b_str.decode(encoding="utf-8")
    print(v, type(v), "\n")
