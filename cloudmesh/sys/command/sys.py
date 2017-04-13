from __future__ import print_function

from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command

from cloudmesh.sys.manage import Command, Git


class SysCommand(PluginCommand):
    @command
    def do_sys(self, args, arguments):
        """
        ::

          Usage:
                sys git commit MESSAGE
                sys git upload
                sys command generate NAME

          This command does some useful things.

          Arguments:
              MESSAGE  the message to commit 
              NAME     the command to generate

          Options:
              -f      specify the file

        """
        print(arguments)

        if arguments.git and arguments.commit:

            msg = arguments.MESSAGE
            Git.commit(msg)

        elif arguments.git and arguments.upload:

            Git.upload()

        elif arguments.command and arguments.generate:

            name = arguments.NAME
            Command.generate(name)
