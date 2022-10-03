def check_str_to_bytes(*args):
    for v in args:
        try:
            b_str = bytes(v, encoding="ascii")
        except UnicodeEncodeError:
            print(
                f"The function can't encode non-ascii symbols ({v}), thus it has stopped"
            )
            return
        print(b_str, type(b_str))


check_str_to_bytes("s", "ааууыыв", "s")
