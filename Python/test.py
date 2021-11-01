def foo(string, *args):
    print(*args)
    print(string, *args)


foo("?")
