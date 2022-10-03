strings = ["разработка", "сокет", "декоратор"]
for v in strings:
    print(v, type(v))

strings[0] = "\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430"
strings[1] = "\u0441\u043e\u043a\u0435\u0442"
strings[2] = "\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440"

for v in strings:
    print(v, type(v))
