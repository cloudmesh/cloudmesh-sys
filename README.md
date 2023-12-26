# Cloudmesh Sys

Cloudmesh sys is a command that allows the generation of new plugin
commands to cmd5. For more details we like you to look at the
`cloudmesh.cmd5` manual and the `cloudmesh.manual` pages at

* <https://github.com/cloudmesh/cloudmesh.cmd5>
* <https://cloudmesh.github.io/cloudmesh-manual>

## Acknowledgments

Continued work was in part funded by the NSF
CyberTraining: CIC: CyberTraining for Students and Technologies
from Generation Z with the awadrd numbers 1829704 and 2200409.



## Manual Page

<!-- START-MANUAL -->
```
Command sys
===========

::

  Usage:
    sys upload
    sys commit MESSAGE
    sys generate NAME [.]
    sys version VERSION
    sys install choco

  This command does some useful things.

  Arguments:
    MESSAGE   the message to commit
    NAME      the command to generate
    VERSION   the version number

  Options:
    -f      specify the file

  Description:
    cms sys generate NAME

        When you execute this command it
        will generate a  directory tree for a command
        with the name

        cloudmesh-NAME

        To install the command you need to

        cd cloudmesh-NAME
        pip install -e .

        or

        pip install .

    cms sys generate  NAME .

        the code will be installed in the current directory. This is
        helpful, if you already are in a directory fof the name
        cloudmesh-NAME, e.g. if you already created it in github and
        like to add a command in that github directory.

    The commands 'version', 'commit' and 'upload'
    are only to be used by Gregor.

    cms version
        The version command adds a new version to the
        VERSION file for cmd5, common, and sys.
        This helps to keep the versions aligned across
        these modules.

    cms commit
        The commit  command adds a new version and commits

    cms upload
        The upload command uploads the new version to pypi

```
<!-- STOP-MANUAL -->