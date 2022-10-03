strings = ["class", "function", "method"]
for v in strings:
    str_b = eval(f"b'{v}'")
    print(str_b, type(str_b))
