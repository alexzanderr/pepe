
from . import cli
import click




from core_dev.shell import run_shell
from core_dev.shell import get_output
from time import sleep

import os
from pathlib import Path
from string import Template

from pepe.core.git import Git
from pepe.core.spinner import SpinnerDots


from rich.console import Console

_con = Console()


from core_dev.aesthetics import *

# import core_dev.shell
# print(core_dev.shell.__file__)
# print(core.shell.__path__)


python_icon = "🐍"

remote_template_repo = "https://github.com/alexzanderr/python-package-project-template"

# just like 'npx create-react-app app'
@cli.command(name="create-python-package")
@click.argument("folder")
@click.option("--python", "-py")
@click.option("--description", "-d")
@click.option("--interactive", "-it", default=False)
def wrapper(folder, python, description, interactive):
    # print(python)
    # print(description)
    # print(interactive)
    color = RGBColors()
    print(f"\nCreating {yellow('python package')} from template:")
    blue_dark_arrow = color.blue_dark("  → ")
    print(blue_dark_arrow + color.cyan(italic(underlined(("https://github.com/alexzanderr/python-package-project-template")))))
    print()


    oldcwd = os.getcwd()
    try:
        create_python_package(folder, python, description)
    except Exception as error:
        _con.print_exception(word_wrap=True)
        os.chdir(oldcwd)
        run_shell("rm -rf python-package-project-template")
        run_shell(f"rm -rf {folder}")
    else:
        print(f"\n{green('Successfully')} created {yellow('python package')} from template. {green(python_icon)}")
        print("\nProject contains:")
        print(blue_dark_arrow + f" Git Repo " + yellow(""))
        # print(blue_dark_arrow + f" Virtual Environment: {get_output()} " + yellow(""))
        print(blue_dark_arrow + " README.md " + yellow(""))
        print(blue_dark_arrow + " and many more ... ")

import subprocess
from typing import Tuple

def create_python_package(folder, python_version, description):
    if folder == ".":
        # then create everything at current workding directory
        print("dot")
    else:
        git_credentials = Git.get_git_credentials()

        username = git_credentials.username
        author_email = git_credentials.email
        package_name = folder

        # Git.clone(remote_template_repo, folder)
        spinner = SpinnerDots(
            message="cloning template ...",
            done_message="cloned template",
            _function=Git.clone,
            _args=(remote_template_repo, folder)
        )
        spinner.animate()
        del spinner

        cwd = os.getcwd()
        os.chdir(folder)

        spinner = SpinnerDots(
            message="removing the old git repo ...",
            done_message="removed the old git repo",
            _function=run_shell,
            _args=("rm -rf .git",) # MUST COMMA
        )
        spinner.animate()
        del spinner

        Git.init()


        def is_in_folders_to_ignore(entity: Path):
            return entity.name in [".git"]

        def rename_all(_path: Path):
            for item in _path.iterdir():
                if item.is_file():
                    # print(item.suffix)
                    if item.suffix in [".png", ".svg"]:
                        continue

                    # print(item.absolute())
                    file_contents = item.read_text()
                    file_contents = Template(file_contents).safe_substitute(
                        USERNAME=username,
                        AUTHOR_EMAIL=author_email,
                        PACKAGE_NAME=package_name,
                        DESCRIPTION=description,
                        HOME=os.environ["HOME"],
                        PYTHON_VERSION=python_version if python_version else "3.10"
                    )
                    item.write_text(file_contents)
                    # print(file_contents)
                else:
                    if is_in_folders_to_ignore(item):
                        continue

                    rename_all(item)


        template_package = Path(".")
        spinner = SpinnerDots(
            message="renaming all files accordingly ...",
            done_message="renamed all",
            _function=rename_all,
            _args=(template_package, )
        )
        spinner.animate()
        del spinner
        print()

        venv_name = os.path.basename(get_output("poetry env info --path"))

        pyrightconfig_json = Path("pyrightconfig.json")
        pyrightconfig_json.write_text(Template(pyrightconfig_json.read_text()).safe_substitute(
            VENV_NAME=venv_name
        ))

        # mv python-package -> folder
        python_package = template_package / "python-package"
        python_package.rename(folder)


        run_shell("poetry install")
        # run_shell("poetry run pip freeze > requirements.txt")



        run_shell("git add .", devnull=True)

        Git.commit("created repo")

        # cd ..
        # os.chdir(cwd)
        # run_shell(f"rm -rf {folder}")

        # spawn virtual env
        # run_shell("poetry shell")

