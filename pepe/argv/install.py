

from . import cli
import click

from pepe.config import PACKAGE_MANAGER
import subprocess


def _install(dev, **kw):

    _install_command = "install"
    if PACKAGE_MANAGER == "poetry":
        _install_command = "add"
    # elif PACKAGE_MANAGER == "pipenv":


    _dev = ""
    if dev:
        _dev = "--dev"


    _packages_list = " ".join(kw["packages"])

    _command = f"{PACKAGE_MANAGER} {_install_command} {_dev} {_packages_list}"
    print("running command:")
    print(_command)

    # execute command
    # exit_code = subprocess.call(_command)
    # if exit_code != 0:
    #     print("oops something is wrong")

    print("command completed successfully")



def install_wrapper(_func):
    _name = _func.__name__
    @cli.command(name=_name)
    @click.option("--dev", is_flag=True, default=False)
    @click.argument('packages', nargs=-1)
    def inner_wrapper(dev, **kw):
        _install(dev, **kw)
    return inner_wrapper

@install_wrapper
def install(dev, **kw):
    pass
    # _install(dev, **kw)


@install_wrapper
def i(dev, **kw):
    pass
    # _install(dev, **kw)

# not working
# cli.add_command(install, name="install")
# cli.add_command(i, name="i")