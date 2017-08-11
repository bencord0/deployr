from __future__ import print_function

import sys

from urllib.parse import urlparse

from .args import parser
from .deploy import deploy_cmd


def main():
    # If the first positional argument is a url,
    # use the default 'deploy' subcommand.
    if len(sys.argv) > 1 and urlparse(sys.argv[1]).scheme:
        sys.argv.insert(1, 'deploy')

    # Choose which sub command to use, or give the user more choices
    args = parser.parse_args()
    if args.subcommand:
        subcmd = {
            'deploy': deploy_cmd,
        }[args.subcommand]

        subcmd(args)
    else:
        parser.print_help()
