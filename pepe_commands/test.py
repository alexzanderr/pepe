

import subprocess as s


def another_func():
    return 123

def main():
    x = another_func()
    s.call("pytest -vv -x -rP --color=yes", shell=True)
    print("test")
    print(x)


# _locals = locals().copy()
# for name, item in _locals.items():
#     if isfunction(item):
#         print("is function: {}".format(item))
#     elif isinstance(item, click.Command):
#         print("command: {}".format(item))

