import logging
import sys
import time

import requests

logger = logging.getLogger(__name__)


def pod_report(appname):
    status = wait_for_pod(appname)

    if status == "Failure":
        logger.error(pod_info["message"])
        sys.exit(1)

    pod_ip = status["podIP"]
    logger.info(f"\n{appname} pod is available at {pod_ip}")


def pod_status(appname):
    # TODO: get this from a config file, or read kubeconfig
    kubernetes_api_url = 'http://localhost:8080'
    pod_api_path = f'/api/v1/namespaces/default/pods/{appname}'
    pod_info = requests.get(f'{kubernetes_api_url}{pod_api_path}').json()

    return pod_info["status"]


def wait_for_pod(appname):
    while True:
        status = pod_status(appname)
        if status["phase"] == "Pending":
            time.sleep(1)
        else:
            break

    return status
