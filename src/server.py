import logging
from datetime import datetime

from chaosmesh.client import Client as ChaosClient
from flask import Flask
from kubernetes import config, client as k8s_client
from kubernetes.client.models.v1_namespace import V1Namespace
from kubernetes.client.models.v1_pod import V1Pod

from sources.src import k8s

# Enable logging for the chaos mesh client
logging.getLogger("chaosmesh")
logging.basicConfig(level=logging.DEBUG)

# Create global clients
logging.info("Loading Kubernetes configuration")
config.load_kube_config("kubeconfig.yaml")
kube_v1_api = k8s_client.CoreV1Api()
chaos_client = ChaosClient(version="v1alpha1")
chaos_namespace: V1Namespace | None = None

# App variables
rce_pods: list[V1Pod] = []

# Create flask app
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == "__main__":
    logging.info("Checking if previous experiment exists")
    k8s_namespaces = kube_v1_api.list_namespace()
    for namespace in k8s_namespaces.items:
        namespace_name = namespace.metadata.name
        if namespace_name.startswith("rce-chaos-"):
            logging.info(f"Previous experiment ${namespace_name} exists, deleting it!")
            kube_v1_api.delete_namespace(name=namespace_name)

    logging.info("Creating namespace for experiment")
    namespace_template = k8s.namespace_template(
        name=f"rce-chaos-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}")
    chaos_namespace = kube_v1_api.create_namespace(namespace_template)

    logging.info("Creating rce pod")
    rce_pod_template = k8s.rce_pod_template("node1", ["-console"])

    rce_pods.append(kube_v1_api.create_namespaced_pod(namespace=chaos_namespace.metadata.name,
                                                      body=rce_pod_template))

    logging.info("Starting flask server")
    app.run()
