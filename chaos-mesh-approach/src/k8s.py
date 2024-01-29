from kubernetes import client

"""
This module contains functions to create kubernetes objects.
"""


def rce_pod_template(node_name: str, image: str, args: list[str] = None):
    """
    Create a pod template for the rce pod.

    :param node_name: The name of the node to schedule the pod on.
    :type node_name: str
    :param image: The image to use.
    :type image: str
    :param args: The arguments to pass to the rce pod.
    :type args: list[str]

    :return: The rce pod template.
    :rtype: client.V1Pod
    """

    pod = client.V1Pod(
        api_version="v1",
        kind="Pod",
        metadata=client.V1ObjectMeta(
            name=node_name,
            labels={
                "app": "rce",
                "rce-node-name": node_name,
            }
        ),
        spec=client.V1PodSpec(
            containers=[
                client.V1Container(
                    name=node_name,
                    image=image,
                    image_pull_policy="Always",
                    args=args if args is not None else [],
                )
            ]
        )
    )

    return pod


def rce_node_port_service_template(node_name: str, ports: list[int] = None):
    """
    Create a node_port service template for the rce pod.

    :param node_name: The name of the node to schedule the pod on.
    :type node_name: str
    :param ports: The ports to expose.
    :type ports: list[int]

    :return: The rce node port service template.
    :rtype: client.V1Service | None
    """

    if ports is None:
        return None

    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            name=node_name,
            labels={
                "app": "rce",
                "rce-node-name": node_name,
            }
        ),
        spec=client.V1ServiceSpec(
            type="NodePort",
            ports=[
                client.V1ServicePort(
                    name=f"port-{port}-{node_name}",
                    # Port for internal communication
                    port=port,
                    # Port that the application is listening on
                    target_port=port,
                    # Port to exposed via the control plane, to avoid conflicts we
                    # let kubernetes choose a free port
                    # node_port=port,
                ) for port in ports if ports is not None
            ],
            selector={
                "app": "rce",
                "rce-node-name": node_name,
            }
        )
    )

    return service


def namespace_template(name: str):
    """
    Create a namespace template.

    :param name: The name of the namespace to create.
    :type name: str

    :return: The namespace.
    :rtype: client.V1Namespace
    """

    namespace = client.V1Namespace(
        api_version="v1",
        kind="Namespace",
        metadata=client.V1ObjectMeta(
            name=name
        )
    )

    return namespace
