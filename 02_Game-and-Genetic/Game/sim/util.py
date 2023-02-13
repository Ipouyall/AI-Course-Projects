from sys import argv


def arg_with_default(arg_index, default):
    if len(argv) > arg_index:
        return argv[arg_index]
    else:
        return default
