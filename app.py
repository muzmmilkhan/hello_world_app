from kubernetes import client, config
from flask import Flask

app = Flask(__name__)

config.load_incluster_config()  # Load the Kubernetes configuration from the cluster

api_instance = client.CoreV1Api()

pod_name = None
try:
    pod_name = open("/var/run/secrets/kubernetes.io/serviceaccount/pod.name", "r").read()
except Exception as e:
    # Handle error if running outside of Kubernetes cluster
    pass

if pod_name:
    pod = api_instance.read_namespaced_pod(name=pod_name, namespace='default')
    container_name = pod.spec.containers[0].name
else:
    container_name = None

@app.route('/')
def hello_world():
    return 'Hello from container {}'.format(container_name)

if __name__ == "__main__":
     app.run(host='0.0.0.0', port=5000)
