### Luxor Technical Test

## Author: Kurniadi Ilham

Welcome to the Luxor Technical Test repository. This project implements a simple controller designed to watch http-server resources defined through a CustomResourceDefinition (CRD).

Prerequisites
Before you begin, make sure you have the following tools installed on your system, you can refer to the documentation of each tools that needs before:

Python: Ensure that Python is installed on your machine. You can download it from python.org.

Minikube: Minikube is a tool that enables you to run Kubernetes clusters locally. Install Minikube by following the instructions at minikube.sigs.k8s.io/docs/start/.

Docker: Docker is used for containerization. Download and install Docker from docker.com.

Kopf: Kubernetes Operator Framework, Installation guide please follow this link, https://kopf.readthedocs.io/en/stable/.


### Section 1: Building http-server source code

We need will build the source code that located in src folder with command,

Working directory: src

```console 
docker build -t luxor-httpserver:v1 .
```

Its because i want to store the image in local, i choose the way to export the image to tar.

```console 
docker image save -o image.tar luxor-httpserver:v1
```

Ater that we need to load the image to minikube, so the image can be load.

```console 
minikube image load image.tar
```

When we successfuly upload the image to minikube, it will show in the list

```console 
minikube image ls
```

### Section 2: Building image for operator 

Working directory: kubernetes/operator

We will build the image for operator that will be used for observe our CRD.

```console 
docker build -t luxor-operator:v1 .
```

we will also doing the export for the docker images and will also load the docker image to minikube with this command,

```console 
docker image save -o image-operator.tar luxor-operator:v1
minikube image load image-operator.tar
```

### Section 3: Deploying the CRD, Kubernetes Operator and also CustomResource.

After everything that we need already loaded to minikube, we will continue with deploying the required things,

## CRD

```console 
kubectl apply -f kubernetes/operator/crd/CustomResourceDefinition.yml
```

## Deploy Operator Permission using RBAC

```console 
kubectl apply -f kubernetes/operator/deploy/rbac
```

## Deploy The Operator

```console 
kubectl apply -f kubernetes/operator/deploy/KubernetesOperator.yml
```

## Deploy CR (demoweb object)

```console 
kubectl apply -f kubernetes/operator/deploy/CustomResource.yml
```

## Check The Operator & The Deployment

```console 
kubectl get pod,svc -n default
```

### Section 4 : Testing the resource that had been deployed

Once all required resources are deployed, check the logs in the deployment of the http server. The http server serves GET /ping and responds with "pong\n".

![Alt text](image-5.png)

Multithreading is employed to enable the http-server to perform GET requests to other similar HTTP servers, providing a unique identifier obtained from the hostname. The response is as follows:

![Alt text](image-6.png)
Pinged http://10.99.169.61/ping - Response: Pong from demoweb-deployment-5657dc974-dsvcz