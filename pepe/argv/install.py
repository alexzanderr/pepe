

# python
import subprocess

# project
## pepe/__init__.py
from . import cli
import click

## pepe.config
from pepe.config import PACKAGE_MANAGER

# 3rd party
from core_dev.aesthetics import *

color = RGBColors()


def _install(dev, **kw):

    _install_command = "install"
    if PACKAGE_MANAGER == "poetry":
        _install_command = "add"
    # elif PACKAGE_MANAGER == "pipenv":

    _dev = ""
    if dev:
        _dev = " --dev"

    _packages_list = " ".join(kw["packages"])

    _command = f"{PACKAGE_MANAGER} {_install_command}{_dev} {_packages_list}"
    print(italic(color.cyan(_command)))

    # execute command
    # exit_code = subprocess.call(_command)
    # if exit_code != 0:
    #     print("oops something is wrong")


def install_command_wrapper(_name: str):
    @cli.command(name=_name)
    @click.option("--dev", is_flag=True, default=False)
    @click.argument('packages', nargs=-1)
    def inner_wrapper(dev, **kw):
        _install(dev, **kw)
    return inner_wrapper



# installing all install commands
_command = "install"
for index in range(1, len(_command) + 1):
    subcommand = _command[:index]
    if subcommand == "in":
        _code = f"_in = install_command_wrapper(\"{subcommand}\")"
        exec(_code)
        continue

    _code = f"{subcommand} = install_command_wrapper(\"{subcommand}\")"
    exec(_code)