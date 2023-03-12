import subprocess
from flask import Flask

app = Flask(__name__)

host_name = None
try:
    # Run the `hostname` command in a shell and capture its output
    output = subprocess.check_output(['hostname'], shell=True) 
    host_name = output.decode() 
except Exception as e:
    # Handle error if running outside of Kubernetes cluster
    pass

@app.route('/')
def hello_world():
    return 'Hello from host {}'.format(host_name)

if __name__ == "__main__":
     app.run(host='0.0.0.0', port=5000)
