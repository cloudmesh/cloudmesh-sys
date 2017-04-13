from __future__ import print_function

from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command

from cloudmesh.sys.manage import Command, Git


class BarCommand(PluginCommand):
    @command
    def do_bar(self, args, arguments):
        """
        ::

          Usage:
                git commit MESSAGE
                git upload
                command generate NAME

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
