# Sklearn Tree for Kubernetes

This takes the 1-sklearn-tree-aws example project, but adapts it to Kubernetes. This third example is designed to show how zero code changes are made, and the adaptions are entirely through config YAML files. 

## Infrastructure Pre-requisites

1. (10 minutes) Set up a Kubernetes cluster of your choice. Minikube, EKS or Bitnami Kubernetes Sandbox work. When your Kubernetes cluster is running, apply the kubeconfig credentials to the environment you are running kubectl from. Use the instructions for the Kubernetes provider chosen above.

2. (2 minutes) Create a namespace on the Kubernetes cluster where the jobs will run.

3. (2 minutes) Data Upload - Create a S3 bucket in the same region you plan to run jobs in and upload in the files from the `/data` folder of this tutorial. 

4. (3 minutes) Create a ECR Repo - Follow the [AWS instructions on creating an ECR repo](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html) and create an ECR repo, keeping the region consistent with the region in which the S3 bucket was created.
 

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

1. Build training job container

    ```
    mlctl train build -c train.yaml
    ```

2. Upload training job container to ECR

    ECR has a custom login script. To start that command, run `aws ecr get-login-password`. If you need to specify an AWS region, [read through the command options](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html#cli-authenticate-registry) in full.

    Once the above command successfully retrieves the credentials, use these commands to upload the docker image to ECR:

    ```
    aws ecr get-login-password | docker login --username AWS --password-stdin <ecr URL>
    docker tag train-image <ecr URL>:train-image
    docker push <ecr URL>:train-image
    ```

3. Configure the training job

    In the `train.yaml` file, update the fields `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` with the right values for your AWS account. This is needed because the training job reads and writes to AWS S3. Support for additional object storage providers is coming soon.

4. Run the training job

    ```
    mlctl train start -c train.yaml
    ```

5. Verify the status of the training job

    ```
    kubectl get pods -n <namespace_name>
    ```

    In order to read the logs of the pod, you can use:

    ```
    kubectl logs -n <namespace_name> <pod_name>
    ```

    After a successful execution, you should see logs similar to this:
    
    ```
    Starting mlctl container
    This is a training job
    Using Kubernetes as a provider
    Selected Kubernetes profile
    Found channel request: input_training
    s3 sagemaker-bucket data/train
    /opt/ml/input/data/training/data.csv
    Retrieved input data
    Files in training directory: ['/opt/ml/input/data/training/data.csv']
      age  weight  height
    0   28     172     183
    1   35     203     161
    2   29     375     172
    3   66     156     191
    4   18     276     161
    Success!
    Found output: s3://sagemaker-bucket/example-3
    /opt/ml/model/ model.pkl
    ```