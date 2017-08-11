import logging
import pathlib
import subprocess
import sys
import tempfile

import requests

from .pods import pod_report


logger = logging.getLogger(__name__)


def deploy_cmd(args):
    logger.info(f"deploy: {args}")

    repository = args.repository
    git_hash = args.git_hash

    if args.appname:
        appname = args.appname
    else:
        # This is a little bit more reliable than os.path.basename
        # as it handles trailing slashes sensibly
        appname = pathlib.Path(repository).parts[-1]

    with tempfile.TemporaryDirectory() as td:
        clonedir = pathlib.Path(td) / appname

        # TODO: set the docker image repository from a configuration file
        docker_tag = f'localhost:5000/{appname}:{git_hash}'

        clone_repo(clonedir, appname, repository, git_hash)

        docker_build(clonedir, docker_tag)
        docker_push(docker_tag)
        kube_apply(clonedir, appname, git_hash)

        pod_report(appname)


def clone_repo(directory, appname, repository, git_hash):
    # TODO: Use a shallow clone
    ret = subprocess.run(['git', 'clone', repository, directory])

    if ret.returncode:
        logger.error(f"Aborting deploy. Failed to clone repo: {repository}")
        sys.exit(ret.returncode)

    ret = subprocess.run(['git', '-C', directory, 'reset', '--hard', git_hash])

    if ret.returncode:
        logger.error(f"Aborting depoloy. Failed to checkout: {git_hash}")
        sys.exit(ret.returncode)


def docker_build(directory, tag):
    ret = subprocess.run(['docker', 'build', '-t', tag, directory])
    if ret.returncode:
        logger.error(f"Aborting deploy. Failed to build {tag}")
        sys.exit(ret.returncode)


def docker_push(tag):
    ret = subprocess.run(['docker', 'push', tag])
    if ret.returncode:
        print(f"Aborting deploy. Failed to push {tag}")
        sys.exit(ret.returncode)


def kube_apply(directory, appname, git_hash):
    with open(directory / 'deployr.yml', 'rt') as pod_template:
        pod_spec = (
            pod_template.read()
                        .replace('NAME', appname)
                        .replace('GITHASH', git_hash)
        )

    ret = subprocess.run(['kubectl', 'apply', '-f', '-'], input=pod_spec.encode())
    if ret.returncode:
        print(f"Aborting deploy. Failed to apply pod spec")
        sys.exit(ret.returncode)
