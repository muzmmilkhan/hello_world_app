from kubernetes import client, config
from flask import Flask

app = Flask(__name__)

config.load_kube_config()  # Load the Kubernetes configuration from the kubeconfig file

api_instance = client.CoreV1Api()

host_name = None
try:
    pod_name = open("/var/run/secrets/kubernetes.io/serviceaccount/pod.name", "r").read()
    pod = api_instance.read_namespaced_pod(name=pod_name, namespace='default')
    command = ['/bin/bash', '-c', 'hostname']  # Bash command to get the hostname of the pod's node
    resp = api_instance.exec_namespaced_pod(name=pod_name, namespace='default', container=pod.spec.containers[0].name, command=command)
    host_name = resp.output.decode().strip()  # Get the output of the command and strip newline characters
except Exception as e:
    # Handle error if running outside of Kubernetes cluster
    pass

@app.route('/')
def hello_world():
    return 'Hello from host {}'.format(host_name)

if __name__ == "__main__":
     app.run(host='0.0.0.0', port=5000)
