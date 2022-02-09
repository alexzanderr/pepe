


import subprocess as s


def another_func():
    return 123

def main():
    x = another_func()
    s.call("echo 'its working'", shell=True)
    print("test")
    print(x)
