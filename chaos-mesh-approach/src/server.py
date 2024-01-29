import logging
from datetime import datetime

from chaosmesh.client import Client as ChaosClient
from flask import Flask, request, jsonify
from kubernetes import config, client as k8s_client
from kubernetes.client.models.v1_namespace import V1Namespace

from instance_manager import K8sInstanceManager, IInstanceManager, IManagedInstance

# Enable logging for the chaos mesh client
logging.getLogger("chaosmesh")
logging.basicConfig(level=logging.DEBUG)

# Create global clients
logging.info("Loading Kubernetes configuration")
config.load_kube_config("kubeconfig.yaml")
kube_v1_api = k8s_client.CoreV1Api()
chaos_client = ChaosClient(version="v1alpha1")
chaos_namespace: V1Namespace | None = None

# Instance manager
instance_manager: IInstanceManager | None = None

# Create flask app
app = Flask(__name__)


def instance_to_json(instance: IManagedInstance):
    """
    Convert an instance to a JSON representation.

    :param instance: The instance to convert.
    :type instance: IManagedInstance

    :return: The JSON representation.
    :rtype: dict[str, any]
    """
    return {
        "name": instance.instance_name,
        "args": instance.args,
        "ports": instance.port_mappings,
    }


@app.route('/')
def hello_world():
    return 'The server is running!\n' + str(instance_manager.get_meta_information())


@app.route("/instances/", methods=['GET', 'POST'])
def instances_create():
    if request.method == 'GET':
        return jsonify(
            [instance_to_json(instance) for instance in instance_manager.instances.values()])

    if request.method == 'POST':
        if not request.is_json:
            return "Request is not JSON!", 400
        json = request.get_json()
        instance_name = json.get("name", None)
        if instance_name is None:
            return "Instance name is missing!", 400
        args = json.get("args", [])
        if args is None:
            return "Instance arguments are missing!", 400
        instance = instance_manager.start_instance(instance_name, args)
        return jsonify(instance_to_json(instance))


@app.route('/instances/<instance_name>', methods=['GET', 'DELETE'])
def instances(instance_name: str):
    instance = instance_manager.get_instance(instance_name)
    if instance is None:
        return f"Instance with name {instance_name} doesn't exist!", 404

    if request.method == 'GET':
        return jsonify(instance_to_json(instance))
    if request.method == 'DELETE':
        # Stop actually deletes the instance, there is no real stop command at the moment
        instance_manager.stop_instance(instance)
        return "Instance stopped", 200


if __name__ == "__main__":
    logging.info("Checking if previous experiment exists")
    k8s_namespaces = kube_v1_api.list_namespace()
    for namespace in k8s_namespaces.items:
        namespace_name = namespace.metadata.name
        if namespace_name.startswith("rce-chaos-"):
            logging.info(f"Previous experiment ${namespace_name} exists, deleting it!")
            kube_v1_api.delete_namespace(name=namespace_name)

    logging.info("Creating instance manager for experiment")
    instance_manager = K8sInstanceManager(
        namespace=f"rce-chaos-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}",
        k8s_client=kube_v1_api)

    logging.info("Starting flask app")
    app.run()
