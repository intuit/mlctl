# Sklearn Tree for Kubernetes

This takes the 1-sklearn-tree-aws example project, but adapts it to Kubernetes. This third example is designed to show how zero code changes are made, and the adaptions are entirely through config YAML files. 

## Infrastructure Pre-requisites

1. (10 minutes) Set up a Kubernetes cluster of your choice. Minikube, EKS or (Bitnami Kubernetes Sandbox)[https://aws.amazon.com/marketplace/pp/prodview-hy5b54ebhfcsm] work. When your Kubernetes cluster is running, apply the kubeconfig to your client. Bitnami has (specific instructions)[https://docs.bitnami.com/aws/infrastructure/kubernetes-sandbox/configuration/configure-local-kubectl/] for the credentials of the Kubeconfig. 

2. (2 minutes) Create a namespace on the Kubernetes cluster where the jobs will run.

3. (2 minutes) Data Upload - Create a S3 bucket in the same region you plan to run jobs in and upload in the files from the `/data` folder of this tutorial. 

4. (3 minutes) Create a ECR Repo - Follow the [AWS instructions on creating an ECR repo](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html) and create an ECR repo, keeping the region consistent with the region in which the S3 bucket was created.

5. (2 minutes) Add AWS credentials to cluster - 

## Install and configure mlctl

1. Installation

Install the latest `dev` version of `mlctl`. The latest releases are available on [PyPi](https://pypi.org/project/mlctl/#history):

    ```
    pip install mlctl==0.0.6.dev1
    ```

2. Point mlctl to your infrastructure

Edit the `provider.yaml`:

- Replace `namespace` with the name of the namespace created in step 2 of the pre requisites.
- Replace the `container_repo` with the repo created in Step 4 of the prereqs. 

The `provider.yaml` file below is an example of how the final file should look. Our ECR repo is in us-east-1, but you could use another region.

    ```
    mlctl_version: 0.1
infrastructure:
  - name: kubernetes
    namespace: mlctl_demo
    container_repo: 123456789.dkr.ecr.us-east2.amazonaws.com/mlctl
resources:
  train: 
    requests:
      memory: "256Mi"
      cpu: "1000m"
    limits:
      memory: "1024Mi"
      cpu: "1000m"
    ```

## Build and Execute Jobs

### Training Job

1. Build and upload training job container

2. Run the training job