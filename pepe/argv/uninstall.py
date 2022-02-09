



from . import cli
import click

def _uninstall(dev, **kw):
    if dev:
        print("dev packages")
    else:
        print("no dev")

    _packages = kw["packages"]
    print("packages:")
    for package in _packages:
        print(package)

@cli.command()
@click.option("--dev", is_flag=True, default=False)
@click.argument('packages', nargs=-1)
def uninstall(dev, **kw):
    _uninstall(dev, **kw)


@cli.command()
@click.option("--dev", is_flag=True, default=False)
@click.argument('packages', nargs=-1)
def rm(dev, **kw):
    _uninstall(dev, **kw)