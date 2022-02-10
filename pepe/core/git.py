
from core_dev.shell import run_shell
from pathlib import Path
from collections import namedtuple



class Git:
    @staticmethod
    def commit(message=None, quiet=True):
        _quiet = " --quiet" if quiet else ""
        _message = " -m '{message}'" if message else ""
        run_shell(f"git commit{_message}{_quiet}")


    @staticmethod
    def init(quiet=True):
        _quiet = " --quiet" if quiet else ""
        run_shell(f"git init{_quiet}")


    @staticmethod
    def clone(repo, folder_name=None, quiet=True):
        _quiet = " --quiet" if quiet else ""
        _folder = " " + folder_name if folder_name else ""

        run_shell(f"git clone {repo}{_folder}{_quiet}")


    @staticmethod
    def load_config():
        # global settings
        gitconfig = Path("/etc/gitconfig")

        if not gitconfig.exists():
            # user settings - home
            gitconfig = Path("~/.gitconfig")

        if not gitconfig.exists():
            # user settings - config folder
            gitconfig = Path("~/.config/git/config")

        if not gitconfig.exists():
            # inside repo config at current dir
            gitconfig = Path(".git/config")

        gitconfig_contents = gitconfig.read_text()
        lines = gitconfig_contents.split("\n")
        return lines


    @staticmethod
    def get_value(lines, key):
        for line in lines:
            if key in line:
                start = line.find("=") + 2
                return line[start:]

    @staticmethod
    def get_git_username(lines):
        return Git.get_value(lines, "name")

    @staticmethod
    def get_git_email(lines):
        return Git.get_value(lines, "email")

    @staticmethod
    def get_git_credentials():
        lines = Git.load_config()
        username = Git.get_git_username(lines)
        email = Git.get_git_email(lines)
        return namedtuple("GitCredentials", ["username", "email"])(username, email)


