from .pods import pod_delete


def delete_cmd(args):
    appname = args.appname
    pod_delete(appname)
