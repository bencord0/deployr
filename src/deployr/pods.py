import requests


def pod_report(appname):
    # TODO: get this from a config file
    kubernetes_api_url = 'http://localhost:8080'
    pod_api_path = f'/api/v1/namespaces/default/pods/{appname}'
    pod_info = requests.get(f'{kubernetes_api_url}{pod_api_path}').json()

    pod_status = pod_info["status"]
    pod_ip = pod_status["podIP"]

    print(f"\n{appname} pod is available at {pod_ip}")
