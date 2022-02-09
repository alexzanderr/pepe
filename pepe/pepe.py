"""
    a pipenv wrapper with a cooler name
"""

import os
import subprocess as s
import argparse
import click
from pathlib import Path

# will never work
# s.call("cd /home/alexzander", shell=True)
# os.chdir("/home/alexzander")
# s.call("la", shell=True, executable="/usr/bin/zsh")


# @click.command()
# @click.option("i", "-i", "--install", help="pepe install | pepe i")
# def pepe(i):
#     print(i)
#     print("pipenv install")



# @click.command()
# @click.argument("install", nargs=-1)
# def install(*what, **kw):
#     print(what, kw)
#     _install()

# @click.command()
# @click.argument("i", nargs=-1)
# def i(*what, **kw):
#     print(what, kw)
#     _install()

# @click.group("cli")
# @click.pass_context
# @click.argument("install")
# def cli(context, install):
#     print(context, install)

# def main():
#     cli(prog_name="cli")

@click.group()
def cli():
    pass


# @cli.command()
# @click.argument("name")
# def extra_arguments(name, **kw):
#     print(name)
#     print(kw)
#     if name == "test":
#         print('test')


# from pepe_commands.test import main

def collect_pepe_user_defined_commands():
    pepe_commands = Path("pepe_commands")
    if pepe_commands.exists():
        for _file in pepe_commands.iterdir():
            _stem = _file.stem
            exec(
f"""
@click.command()
def {_stem}():
    from pepe_commands.{_stem} import main
    main()
cli.add_command({_stem}, name="{_stem}")
""")


collect_pepe_user_defined_commands()

if __name__ == '__main__':
    cli()