## Chaos Mesh Approach for RCE Tests in Kubernetes

The Chaos Mesh Approach provides an alternative to WinDivert, focusing on replicating Remote Component Environment (RCE)
tests on real clusters managed by Kubernetes (K8s).

As the native Instance Management (IM) component of RCE isn't initially designed for Kubernetes, we've seamlessly
adapted it to function within a K8s environment. To achieve this, we've implemented a small REST API responsible for
initiating and terminating RCE instances on K8s. This API is then utilized by the IM component to manage RCE.

The rationale behind building a separate API is that Chaos Mesh does not inherently offer a Java client. Therefore, it
was more straightforward to encapsulate the Chaos Mesh client as a REST API than to implement a Java client for Chaos
Mesh. Thus, this API not only handles the starting and stopping of RCE instances but also manages Chaos Mesh, allowing
for the
simulation of network failures within your Kubernetes cluster. This unified approach enables you to control both RCE
instances and Chaos Mesh through a single API endpoint.

## How it Works

Chaos Mesh Approach utilizes Chaos Mesh to simulate network failures within your Kubernetes cluster, allowing you to
closely observe the behavior of RCE instances.
The approach involves leveraging existing RCE test cases, with a particular focus on adapting the Instance Management
Component (IM) implementation.
This modification ensures that RCE instances are not started locally but rather on the Kubernetes cluster. Despite this
relocation, the connection is maintained through RCE's SSH connection. For this the REST API ensures that the SSH
connections are made available for external access.

## Getting Started

To use the Chaos Mesh integration, ensure you have a configured Kubernetes (K8S) cluster and Chaos Mesh installed.
Follow the installation instructions provided [here](https://chaos-mesh.org/docs/quick-start). If you're considering
using Chaos Mesh in a production environment, it is recommended to opt for the Helm installation method,
detailed [here](https://chaos-mesh.org/docs/production-installation-using-helm/).

### Prerequisites:

- **Kubernetes Cluster:** Have a configured K8S cluster ready. If you don't have one, the easiest way to set up a
  Kubernetes cluster locally is through Minikube. Alternatively, you can use production-grade clusters from third-party
  services such as AWS, Azure, GCP, etc. For on-premise setups, options like K3S, MicroK8S, RKE2, etc., can be
  considered.
- **Chaos Mesh:** Chaos Mesh is a cloud-native Chaos Engineering platform that orchestrates chaos on Kubernetes

### Installation:

1. Clone the repository and navigate to the `chaos-mesh-approach` directory.
2. Create a virtual environment and install the dependencies:

```shell
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

3. Create a kubeconfig.yaml file in the `chaos-mesh-approach` directory that contains the configuration for your
   Kubernetes cluster. **The kubeconfig.yaml is expected to be in the root of your current working directory.**
4. Start the REST API server:

```shell
$ python3 src/server.py
```

## Configuration

As this is a proof-of-concept, the configuration is currently hard-coded in multiple places.
The following configuration are available:

- `K8S-CONFIG`: The path to the kubeconfig.yaml file. Defaults to `kubeconfig.yaml`.
- `K8S-NAMESPACE`: The namespace in which the RCE instances are started. Defaults
  to `rce-chaos-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}`.
- `K8S-IMAGE`: The Docker image used for the RCE instances. Defaults to `localhost:32000/s0pex/rce-10.5.0:latest`.

**Best is to use string replace and replace all occurrences of the above default values with your desired values.**

## API
The API is a simple REST API with the following endpoints:
- `GET /`: Returns a simple welcome message.
- `GET /instances`: Returns a list of all currently running RCE instances.
- `GET /instances/<instance-name>`: Returns the status of the RCE instance with the given name.
- `POST /instances`: Starts a new RCE instance. Payload: `{"name": "instance-name", "args": ["array", "of", "args"]}`
- `DELETE /instances/<instance-name>`: Stops the RCE instance with the given name. Stopping the instance will also
  delete the pod.


## Known Issues
- The RCE instances and namespaces are not cleaned up automatically but either on a new start of the API server or by
  manually deleting the namespaces.
- Currently, there is no way to manage multiple parallel tests as only a single namespace is used. Optimally a new
  namespace would be created for each test and deleted after the test is finished.
- The Chaos Mesh API is not completed and only a single network tests for timeouts is implemented.
- Zero Fault Tolerance, if something goes wrong the API server will be undefined behavior.
