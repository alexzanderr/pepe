
from pepe import cli


# these commands must be imported
# otherwise you will not see them
# even if they are defined
from .install import i, install
from .uninstall import rm, uninstall
from .shell import s, shell
from .create import create_python_package
