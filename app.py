from kubernetes import client, config
from flask import Flask

app = Flask(__name__)

config.load_incluster_config()  # Load the Kubernetes configuration from the cluster

api_instance = client.CoreV1Api()

pod_name = config.pod_name  # Get the name of the current pod

pod = api_instance.read_namespaced_pod(name=pod_name, namespace='default')

container_name = None

for container in pod.spec.containers:
    if container.env is not None:
        for env_var in container.env:
            if env_var.name == 'MY_CONTAINER_NAME_ENV_VARIABLE':
                container_name = env_var.value

@app.route('/')
def hello_world():
    return 'Hello from container {}'.format(container_name)

