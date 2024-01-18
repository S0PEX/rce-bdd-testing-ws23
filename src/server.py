import logging
from datetime import datetime

from chaosmesh.client import Client as ChaosClient
from flask import Flask
from kubernetes import config, client as k8s_client
from kubernetes.client.models.v1_namespace import V1Namespace
from kubernetes.client.models.v1_pod import V1Pod

from src import k8s
from src.instance_manager import K8sInstanceManager, IInstanceManager, IManagedInstance

# Enable logging for the chaos mesh client
logging.getLogger("chaosmesh")
logging.basicConfig(level=logging.DEBUG)

# Create global clients
logging.info("Loading Kubernetes configuration")
config.load_kube_config("kubeconfig.yaml")
kube_v1_api = k8s_client.CoreV1Api()
chaos_client = ChaosClient(version="v1alpha1")
chaos_namespace: V1Namespace | None = None

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

    logging.info("Creating instance manager for experiment")
    instance_manager: IInstanceManager = K8sInstanceManager(
        namespace=f"rce-chaos-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}",
        k8s_client=kube_v1_api)

    logging.info("Starting instances")
    rce_pods: list[IManagedInstance] = []
    for i in range(0, 2):
        rce_pods.append(instance_manager.start_instance(f"rce-{i}"))

    # Wait for input to stop the experiment
    input("Press Enter to stop the experiment...")

    logging.info("Stopping instances")
    for rce_pod in rce_pods:
        instance_manager.stop_instance(rce_pod)

    logging.info("Experiment finished")
