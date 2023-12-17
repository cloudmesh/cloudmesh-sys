"""
Managing the cmd5 system installation and package distribution
"""
import os
import textwrap
from pathlib import Path

from cloudmesh.common.Shell import Shell
from cloudmesh.common.console import Console
from cloudmesh.common.util import banner
from cloudmesh.common.util import readfile
from cloudmesh.common.util import writefile

# from cloudmesh.sys.__version__ import version

version = "5.0.0"


class Sys:
    """
    Class to generate cmd5 command templates
    """

    @classmethod
    def generate(cls, name):
        """
        Generate a command template with the given name
        :param name: the name of the command
        :return:
        """

        if name.startswith("cloudmesh-"):
            name = name.replace("cloudmesh-", "")

        command = name
        package = f"cloudmesh-{name}"
        Command = name.capitalize()

        print(command)
        print(package)
        print(command)

        excludes = ["abc", "cmd5", "common", "bumpversion", "sys"]
        if name in excludes:
            Console.error("You can not name the cms command " + ", ".join(excludes))
            return ""

        if os.path.exists(package):
            Console.error(
                f"The command director {package} exists in the current dir. Use a different command name, or delete {package}"
            )
            return ""

        try:
            os.system(f"git clone https://github.com/cloudmesh/cloudmesh-bar {package}")
        except Exception as e:  # noqa: F841
            Console.error(str(e))
            return ""

        def generate_bumpversion(version="5.0.0"):
            script = textwrap.dedent(
                f"""
            bumpversion:
            - VERSION
            - src/cloudmesh/{command}/__version__.py
            - src/cloudmesh/{command}/__init__.py
            """
            )
            return script

        def replace_in_file(filename, old_text, new_text):
            content = readfile(filename)
            content = content.replace(old_text, new_text)
            writefile(filename, content)

        def delete(path, pattern):
            files = Path(path).glob(pattern)
            for file in files:
                file.unlink()

        for pattern in [
            "*.zip",
            "*.egg-info",
            "*.eggs",
            "build",
            "dist",
            ".tox",
            "*.whl",
            "**/__pycache__",
            "**/*.pyc",
            "**/*.pye",
        ]:
            delete("./{package}/", pattern)

        path = Path(f"{package}/.git").resolve()
        Shell.rmdir(path)

        replace_in_file(f"{package}/pyproject.toml", "bar", f"{command}")

        os.rename(f"{package}/src/cloudmesh/bar", f"{package}/src/cloudmesh/{command}")

        os.rename(
            f"{package}/src/cloudmesh/{command}/command/bar.py",
            f"{package}/src/cloudmesh/{command}/command/{command}.py",
        )
        os.rename(
            f"{package}/src/cloudmesh/{command}/bar.py",
            f"{package}/src/cloudmesh/{command}/{command}.py",
        )

        replace_in_file(
            f"{package}/src/cloudmesh/{command}/command/{command}.py",
            "Bar",
            f"{Command}",
        )

        replace_in_file(
            f"{package}/src/cloudmesh/{command}/command/{command}.py",
            "bar",
            f"{command}",
        )

        replace_in_file(
            f"{package}/src/cloudmesh/{command}/{command}.py",
            "Bar",
            f"{Command}",
        )

        replace_in_file(
            f"{package}/src/cloudmesh/{command}/{command}.py",
            "bar",
            f"{command}",
        )

        replace_in_file(f"{package}/Makefile", "bar", f"{command}")
        replace_in_file(f"{package}/README.md", "bar", f"{command}")

        writefile(f"{package}/bumpversion.yaml", generate_bumpversion(version=version))


class Git(object):
    """
    Git management for the preparation to upload the code to pypi
    """

    pypis = ["cloudmesh-common", "cloudmesh-cmd5", "cloudmesh-sys"]
    commits = pypis + ["cloudmesh-bar"]

    # , "cloudmesh-rest"]
    # "cloudmesh-robot"]

    @classmethod
    def upload(cls):
        """
        upload the code to pypi
        :return:
        """

        banner("CREATE DIST")
        for p in cls.pypis:
            try:
                os.system(f"cd {p}; make dist")
            except Exception as e:
                Console.error("can not create dist " + p)
                print(e)

        banner("UPLOAD TO PYPI")
        for p in cls.pypis:
            try:
                os.system(f"cd {p}; make upload")
            except Exception as e:
                Console.error("can upload " + p)
                print(e)

    @classmethod
    def commit(cls, msg):
        """
        commit the current code to git
        :param msg:
        :return:
        """

        banner("COMMIT " + msg)
        for p in cls.commits:
            banner("repo " + p)
            os.system(f'cd {p}; git commit -a -m "{msg}"')
            os.system(f"cd {p}; git push")


class Version(object):
    """
    set the version number of all base packages
    """

    @classmethod
    def set(cls, version):
        """
        set the version number
        :param version: the version as text string
        :return:
        """
        for repo in Git.commits:
            print(repo, "->", version)
            writefile(os.path.join(repo, "VERSION"), version)
