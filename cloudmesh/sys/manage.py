import os
import shutil
from distutils.dir_util import copy_tree
from pprint import pprint

from cloudmesh.common.util import banner


class Command(object):
    @classmethod
    def generate(cls, name):

        data = {
            "command": name,
            "package": "cloudmesh.{}".format(name)
        }

        pprint(data)

        os.system("rm -rf  cloudmesh.gregor")
        try:
            os.system("git clone https://github.com/cloudmesh/cloudmesh.bar")
        except:
            pass

        os.system("cd cloudmesh.bar; make clean")
        copy_tree("cloudmesh.bar", "{package}".format(**data))
        shutil.rmtree("{package}/.git".format(**data))
        os.system('sed -ie "s/bar/{command}/g" {package}/setup.py'.format(**data))
        os.rename("{package}/cloudmesh/bar/command/bar.py".format(**data),
                  "{package}/cloudmesh/bar/command/{command}.py".format(**data))
        os.rename("{package}/cloudmesh/bar".format(**data),
                  "{package}/cloudmesh/{command}".format(**data))
        shutil.rmtree('{package}/cloudmesh/foo'.format(**data))


class Git(object):
    @classmethod
    def upload(cls):

        banner("CREATE DIST")
        for p in ["cloudmesh.common", "cloudmesh.cmd5", "cloudmesh.rest", "cloudmesh.sys"]:
            os.system("cd {}; make dist".format(p))

        banner("UPLOADE TO PYPI")
        for p in ["cloudmesh.common", "cloudmesh.cmd5", "cloudmesh.sys"]:  # , "cloudmesh.rest"]:
            os.system("cd {}; make upload".format(p))

    @classmethod
    def commit(cls, msg):

        banner("COMMIT " + msg)
        for p in ["cloudmesh.common", "cloudmesh.cmd5", "cloudmesh.rest", "cloudmesh.rest"]:
            banner("repo " + p)
            os.system('cd {}; git commit -a -m "{}"'.format(p, msg))
            os.system('cd {}; git push'.format(p))
