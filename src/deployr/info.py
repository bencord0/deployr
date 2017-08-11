from .pods import pod_report


def info_cmd(args):
    appname = args.appname
    pod_report(appname)
