
"""
    pepe create-... stuff like npx create-..
"""


# python
import sys
import os
import subprocess
from time import sleep
from typing import Tuple
from pathlib import Path
from string import Template
# 3rd party packages


import click
from core_dev.shell import run_shell
from core_dev.shell import get_output
from core_dev.icons import Icons
from core_dev.aesthetics import *
from rich.console import Console


# pepe project
# pepe/argv/__init__.py
from . import cli
from . import PROGRAM_NAME

# pepe/core/__init__.py
from pepe.core import Git
from pepe.core import SpinnerDots





_con = Console()
color = RGBColors()




# import core_dev.shell
# print(core_dev.shell.__file__)
# print(core.shell.__path__)



remote_template_repo = "https://github.com/alexzanderr/python-package-project-template"


def cyan_italic(_string: str) -> str:
    return color.cyan(italic(_string))


def __exit(_code: int = 0):
    _colored_code = green(_code)
    _message = green("success")
    if _code != 0:
        _colored_code = red(_code)
        _message = red("error")

    print(f"\n{cyan_italic(PROGRAM_NAME)} exited with code {_colored_code}. ({italic(_message)})")
    # print(sys.argv)
    sys.exit(_code)


# just like 'npx create-react-app app'
@cli.command(name="create-python-package")
@click.argument("folder")
@click.option("--python", "-py", default="3.10")
@click.option("--description", "-d", default="no description available for the package")
@click.option("--interactive", "-it", default=False)
@click.option("--force-delete", "-fd", is_flag=True, default=False)
def wrapper(folder, python, description, interactive, force_delete):
    _exit_code = 0

    print()

    _folder_colored = cyan_italic(folder)
    _exa_tree_command = "./bin/exa --tree --icons --all --ignore-glob='.git|.hg|.hglf|.venv|venv|*-venv|*_venv|__pycache__|.pytest_cache|*font-awesome*'"
    _folder = Path(folder)


    if _folder.exists():
        print(f"{yellow('WARNING')}: folder '{_folder_colored}' already {red('exists')}.")
        print(f"Aborted {italic(yellow('<create-python-package>'))} command.")
        print()
        print(f"Here is a tree representation of the project '{_folder_colored}':")
        run_shell(_exa_tree_command + f" {_folder}")
        _exit_code = 1
        __exit(_exit_code)


    # print(python)
    # print(description)
    # print(interactive)
    print(f"Creating {yellow('python package')} from template:")
    blue_dark_arrow = color.blue_dark("  →  ")
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
        print(f"\n{green('Successfully')} created {yellow('python package')} from template. {green(Icons.python)}")
        print("\nProject contains:")
        print(blue_dark_arrow + f"Git Repo " + yellow(""))
        # print(blue_dark_arrow + f" Virtual Environment: {get_output()} " + yellow(""))
        print(blue_dark_arrow + "README.md " + yellow(""))
        print(blue_dark_arrow + "and many more ... ")

    __exit(_exit_code)

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
                        PYTHON_VERSION=python_version
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

