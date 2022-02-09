

from . import cli
import click

def _shell(**kw):
    print(kw)
    print("launching subshell at cwd")
    # _packages = kw["packages"]
    # print("packages:")
    # for package in _packages:
    #     print(package)

def shell_wrapper(_func):
    @cli.command(name=_func.__name__)
    # @click.option("--dev", is_flag=True, default=False)
    # @click.argument('packages', nargs=-1)
    def inner_wrapper(**kw):
        _shell(**kw)
    return inner_wrapper


@shell_wrapper
def shell(**kw):
    pass


@shell_wrapper
def s(**kw):
    pass