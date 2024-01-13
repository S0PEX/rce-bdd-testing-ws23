# RCE BDD Testing Winter-term 2023/24

This repository contains the source code for the RCE BDD Testing course in the winter-term 2023/24.

## Prerequisites & Getting Started
To run the tests and examples in this repository, you need to install the following tools:
- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Buildah](https://buildah.io/)

**We recommend to use a Linux distribution to run the tests and examples.**

Additionally, to run network tests, you need to have access to a Kubernetes cluster.
If you do not have access to a Kubernetes cluster, you can use [Minikube](https://minikube.sigs.k8s.io/docs/) or [Kind](https://kind.sigs.k8s.io/).
Otherwise, you can use a managed Kubernetes cluster from a cloud provider like [AWS](https://aws.amazon.com/de/eks/), [Azure](https://azure.microsoft.com/de-de/services/kubernetes-service/), or [Google Cloud](https://cloud.google.com/kubernetes-engine).

**Note:** As most network tests are build on top of [Chaos Mesh](https://chaos-mesh.org/), you need to install Chaos Mesh on your Kubernetes cluster.
To install Chaos Mesh, please follow the [quick start](https://chaos-mesh.org/docs/quick-start/).

## Repository Structure
This repository is structured as follows:
- `docs`: Contains the documentation for this repository
- `images`: Contains the Dockerfiles for the Docker images used in this repository

## Contributing
We welcome contributions to this repository. Please ensure that you have installed the following tools:
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)
- [Buildah](https://buildah.io/)

To contribute to this repository, please follow these steps:
1. Fork this repository
2. Clone your forked repository
3. Create a new branch
4. Make your changes
5. Push your changes to your forked repository
6. Create a pull request

To ensure code quality, please run the following commands before pushing your changes:
```bash
$ pre-commit run --all-files
```

### Setting up pre-commit hooks
To set up the pre-commit hooks, please run the following commands:
```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install pre-commit
$ pre-commit install
$ pre-commit install -t pre-commit -t commit-msg
```

## License
This repository is licensed under the [MIT License](LICENSE).