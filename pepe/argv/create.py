
from . import cli
import click

from core.shell import run_shell
from time import sleep

import os
from pathlib import Path
from string import Template



remote_template_repo = "https://github.com/alexzanderr/python-package-project-template"

# just like 'npx create-react-app app'
@cli.command(name="create-python-package")
@click.argument("folder")
def wrapper(folder):
    oldcwd = os.getcwd()
    try:

    except Exception as error:
        print(error)
        os.chdir(oldcwd)
        run_shell("rm -rf python-package-project-template")
        run_shell(f"rm -rf {folder}")


def create_python_package(folder):
    print("creating ... ")
    if folder == ".":
        # then create everything at current workding directory
        print("dot")
    else:
        pass
        print("creating the folder: {}".format(folder))

        username = "alexzadnerr"
        author_email = "alexxander18360@gmail.com"
        package_name = "demo"
        description = "asdb hadauisyhgvdauiosdvasvgyhudasdf ol;bhjasdiofbghuashuioasdg yioufasdgiouyasdfgyhiouasdfgyhiuasdfgyigyuiasdfgyhuiadfsasdfghijouuasdfghijoasdfghijoasdfghjooasdfghjioadfsghjioasdfghjioadfsasdfghijouasdfghijoghioasdf"

        run_shell(f"git clone {remote_template_repo}")
        cwd = os.getcwd()
        os.chdir("python-package-project-template")
        run_shell("rm -rfv .git")
        run_shell("git init")
        run_shell("git add .")
        run_shell("git commit -m 'created repo'")


        def riterdir(_path: Path):
            for item in _path.iterdir():
                if item.is_file():
                    print(item.suffix)
                    if item.suffix in [".png", ".svg"]:
                        continue

                    print(item.absolute())
                    file_contents = item.read_text()
                    file_contents = Template(file_contents).safe_substitute(
                        USERNAME=username,
                        AUTHOR_EMAIL=author_email,
                        PACKAGE_NAME=package_name,
                        DESCRIPTION=description,
                        HOME=os.environ["HOME"],
                        VENV_NAME="pepe-UNum-4dU-py3.10",
                        PYTHON_VERSION="3.10"
                    )
                    item.write_text(file_contents)
                    print(file_contents)
                else:
                    if item.name == ".git":
                        continue
                    riterdir(item)

        template_package = Path(".")
        riterdir(template_package)

        # mv python-package -> folder
        python_package = template_package / "python-package"
        python_package.rename(folder)

        # cd ..
        os.chdir(cwd)
        # cwd == "pepe"

        # mv python-package-project-template -> folder
        template_package.rename(folder)

        os.chdir(folder)



        run_shell("poetry install")
        run_shell("poetry shell")

