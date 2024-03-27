def modify_tuple(in_tup: tuple) -> tuple:
    print(2, id(in_tup))
    in_tup = tuple(it.title() for it in in_tup)
    print(3, id(in_tup))
    return in_tup

if __name__ == '__main__':
    tup = ("bert", "albert")
    print(1, id(tup))
    tup = modify_tuple(tup)
    print(4, id(tup))
    print(tup)
