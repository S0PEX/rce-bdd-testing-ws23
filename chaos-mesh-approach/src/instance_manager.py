import logging
from abc import ABC, abstractmethod

from kubernetes import client

from k8s import namespace_template, rce_pod_template, rce_node_port_service_template

_logger = logging.getLogger(__name__)


class IManagedInstance(ABC):
    """
    An interface for a managed instance.

    :param instance_name: The name of the instance.
    :type instance_name: str
    :param args: The arguments to pass to the instance.
    :type args: list[str]
    :param port_mappings: The port mappings of the instance.
    :type port_mappings: dict[str, int]
    """

    def __init__(self, instance_name: str, args: list[str] = None,
                 port_mappings: dict[str, int] = None):
        """
        Create a new managed instance.

        :param instance_name: The name of the instance.
        :type instance_name: str
        :param args: The arguments to pass to the instance.
        :type args: list[str]
        :param port_mappings: The port mappings of the instance.
        :type port_mappings: dict[str, int]

        :return: The managed instance.
        :rtype: ManagedInstance
        """
        self._instance_name = instance_name
        self._args = [] if args is None else args
        self._port_mappings = {} if port_mappings is None else port_mappings
        pass

    @property
    def instance_name(self) -> str:
        """
        Name of the instance.

        :getter: Get the name of the instance.
        :type: str
        """
        return self._instance_name

    @property
    def args(self) -> list[str]:
        """
        Arguments of the instance.

        :getter: Get the arguments of the instance.
        :type: list[str]
        """
        return self._args

    @property
    def port_mappings(self) -> dict[str, int]:
        """
        Port mappings of the instance.

        :getter: Get the port mappings of the instance.
        :type: dict[str, int]
        """
        return self._port_mappings


class K8sManagedInstance(IManagedInstance):
    """
    A managed instance running on kubernetes.

    :param instance_name: The name of the instance.
    :type instance_name: str
    :param namespace: The namespace to create instances in.
    :type namespace: str
    :param args: The arguments to pass to the instance.
    :type args: list[str]
    :param port_mappings: The port mappings of the instance.
    :type port_mappings: dict[str, int]
    """

    def __init__(self, instance_name: str, namespace: str, args: list[str] = None,
                 port_mappings: dict[str, int] = None):
        """
            Create a new managed instance.

            :param instance_name: The name of the instance.
            :type instance_name: str
            :param namespace: The namespace to create instances in.
            :type namespace: str
            :param args: The arguments to pass to the instance.
            :type args: list[str]
            :param port_mappings: The port mappings of the instance.
            :type port_mappings: dict[str, int]

            :return: The managed instance.
            :rtype: ManagedInstance
            """
        super().__init__(instance_name, args, port_mappings)
        self._namespace = namespace


class IInstanceManager(ABC):
    """
    An interface for an instance manager.
    """

    def __init__(self):
        """
        Create a new instance manager.

        :return: The instance manager.
        :rtype: InstanceManager
        """

        self._instances: dict[str, IManagedInstance] = {}
        self._meta_information: dict[str, str] = {}
        pass

    @property
    def instances(self) -> dict[str, IManagedInstance]:
        """
        Instances managed by the instance manager.

        :getter: Get the instances managed by the instance manager.
        :type: dict[str, IManagedInstance]
        """
        return self._instances

    def get_instance(self, instance_name: str) -> IManagedInstance | None:
        """
        Get an instance by name.

        :param instance_name: The name of the instance.
        :type instance_name: str

        :return: The instance.
        :rtype: ManagedInstance | None
        """
        return self._instances.get(instance_name, None)

    @abstractmethod
    def start_instance(self, instance_name: str, args: list[str] = None) -> IManagedInstance:
        """
        Start a new instance.

        :param instance_name: The name of the instance.
        :type instance_name: str
        :param args: The arguments to pass to the instance.
        :type args: list[str]

        :return: The managed instance.
        :rtype: ManagedInstance
        """
        pass

    @abstractmethod
    def stop_instance(self, instance: IManagedInstance):
        """
        Stop an instance.

        :param instance: The instance to stop.
        :type instance: ManagedInstance
        """
        pass

    def get_meta_information(self) -> dict[str, str]:
        """
        Get meta information about the instance manager.

        :return: The meta information.
        :rtype: dict[str, str]
        """
        return self._meta_information


class K8sInstanceManager(IInstanceManager):
    """
    An instance manager for running instances on kubernetes as pods.

    :param namespace: The namespace to create instances in.
    :type namespace: str
    :param k8s_client: The kubernetes client to use.
    :type k8s_client: client.CoreV1Api
    :param rce_image: The rce image to use.
    :type rce_image: str
    """

    def __init__(self, namespace: str, k8s_client: client.CoreV1Api,
                 rce_image: str = "localhost:32000/s0pex/rce-10.5.0:latest"):
        """
        Create a new instance manager.

        :param namespace: The namespace to create instances in.
        :type namespace: str
        :param k8s_client: The kubernetes client to use.
        :type k8s_client: client.CoreV1Api
        :param rce_image: The rce image to use.
        :type rce_image: str

        :return: The instance manager.
        :rtype: InstanceManager
        """
        super().__init__()
        self._namespace = namespace
        self._k8s_client = k8s_client
        self._rce_image = rce_image

        # Initialize the namespace
        _logger.debug(f"Creating namespace {self._namespace}")
        namespace_tmplt = namespace_template(self._namespace)
        self._k8s_client.create_namespace(namespace_tmplt)
        _logger.debug(f"Created namespace {self._namespace}")

        self._meta_information["namespace"] = self._namespace
        self._meta_information["rce_image"] = self._rce_image

    def start_instance(self, instance_name: str, args: list[str] = None) -> IManagedInstance:
        """
        Start a new instance.

        :param instance_name: The name of the instance.
        :type instance_name: str
        :param args: The arguments to pass to the instance.
        :type args: list[str]

        :return: The managed instance.
        :rtype: ManagedInstance
        """
        internal_instance_name = f"rce-pod-{instance_name}"
        pod_tmplt = rce_pod_template(internal_instance_name, self._rce_image, args)

        _logger.debug(f"Creating pod {instance_name}")
        pod = self._k8s_client.create_namespaced_pod(self._namespace, pod_tmplt)
        _logger.debug(f"Created pod {pod}")

        _logger.debug(f"Exposing instance {instance_name} to via NodePort")
        node_port_service_tmplt = rce_node_port_service_template(internal_instance_name,
                                                                 [20001, 31005])
        service = self._k8s_client.create_namespaced_service(self._namespace,
                                                             node_port_service_tmplt)
        port_mappings = {
            "rce": service.spec.ports[0].node_port,
            "ssh": service.spec.ports[1].node_port
        }
        _logger.debug(
            f"Exposed instance {instance_name} to via NodePort with port mappings {port_mappings}")

        instance = K8sManagedInstance(instance_name, self._namespace, args, port_mappings)
        self._instances[instance_name] = instance
        return instance

    def stop_instance(self, instance: IManagedInstance) -> None:
        """
        Stop an instance.

        :param instance: The instance to stop.
        :type instance: ManagedInstance

        :return: None
        """
        _logger.debug(f"Deleting pod {instance.instance_name}")
        self._k8s_client.delete_namespaced_pod(f"rce-pod-{instance.instance_name}", self._namespace)
        _logger.debug(f"Deleted pod {instance.instance_name}")
        self._instances.pop(instance.instance_name)
