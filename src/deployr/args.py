import argparse


parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

deploy_parser = subparsers.add_parser("deploy")
deploy_parser.add_argument(
    "repository", help="e.g. https://github.com/bencord0/scrumblr")
deploy_parser.add_argument("git_hash", nargs="?", default="master")
deploy_parser.add_argument("-a", "--appname")

info_parser = subparsers.add_parser("info")
info_parser.add_argument("appname")
