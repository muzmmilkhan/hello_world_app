from flask import Flask

app = Flask(__name__)

host_name = None
try:
    command = ['/bin/bash', '-c', 'hostname']  # Bash command to get the hostname of the pod's node
    host_name = command  # Get the output of the command and strip newline characters
except Exception as e:
    # Handle error if running outside of Kubernetes cluster
    pass

@app.route('/')
def hello_world():
    return 'Hello from host {}'.format(host_name)

if __name__ == "__main__":
     app.run(host='0.0.0.0', port=5000)
