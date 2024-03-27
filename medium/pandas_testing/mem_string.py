def modify_string(string: str) -> str:
    print(2, id(string))
    string = string.title()
    print(3, id(string))
    return string

if __name__ == '__main__':
    string = "bert albert"
    print(1, id(string))
    string = modify_string(string)
    print(4, id(string))
    print(string)
