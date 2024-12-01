def recurse_on_iter(func):
    def wrapper(*args, **kwargs):
        try:
            for item in iter(args[1]):
                func(args[0], item, *args[2:], **kwargs)
        except TypeError:
            if None in args:
                return
            func(*args, **kwargs)
    return wrapper