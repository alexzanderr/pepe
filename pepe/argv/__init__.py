
from pepe import cli
from pepe import PROGRAM_NAME


# these commands must be imported
# otherwise you will not see them
# even if they are defined
from .install import *
from .uninstall import rm, uninstall
from .shell import s, shell
from .create import *

# print(globals())

# if i remove all from here
# lsp would give me an error with cli.command underlined
# meaning that is not found
__all__ = []
_command = "install"
for index in range(1, len(_command) + 1):
    subcommand = _command[:index]
    if subcommand == "in":
        # exec("__all__.append(\"_in\")")
        continue

    __all__.append(subcommand) # type: ignore

