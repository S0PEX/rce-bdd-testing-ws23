from kubernetes import client

"""
This module contains functions to create kubernetes objects.
"""

_RCE_IMAGE_MAME = "localhost:32000/s0pex"


def rce_pod_template(node_name: str, args: list[str] = None, rce_version: str = "10.5.0",
                     image_version: str = "latest"):
    """
    Create a pod template for the rce pod.

    :param node_name: The name of the node to schedule the pod on.
    :type node_name: str
    :param args: The arguments to pass to the rce pod.
    :type args: list[str]
    :param rce_version: The version of rce to use.
    :type rce_version: str
    :param image_version: The version of the rce image to use.
    :type image_version: str

    :return: The rce pod template.
    :rtype: client.V1Pod
    """

    pod = client.V1Pod(
        api_version="v1",
        kind="Pod",
        metadata=client.V1ObjectMeta(
            name=f"rce-{node_name}",
            labels={
                "app": "rce",
                "rce-node-name": node_name,
                "rce-version": rce_version
            }
        ),
        spec=client.V1PodSpec(
            containers=[
                client.V1Container(
                    name="rce",
                    image=f"{_RCE_IMAGE_MAME}/rce-{rce_version}:{image_version}",
                    image_pull_policy="Always",
                    args=args if args is not None else [],
                )
            ]
        )
    )

    return pod


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
