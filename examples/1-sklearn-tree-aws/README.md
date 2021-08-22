# Sklearn Tree for AWS SageMaker

This is an example project which builds small SKlearn Decision Tree model to create jobs with SageMaker. 

## Pre-requisites

1. (3 minutes) awscli - To run mlctl with AWS, as end user, you will need to AWS CLI installed and authenticated. The most up to date instructions can be found on the [AWS CLI install page](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html). 

2. (10 minutes) Role assignments - To run a SageMaker job, you need to create an execution role. The role gives and limits which permissions the jobs created by mlctl can do. [This guide on the SageMaker docs](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html) include instructions for creating roles with both SageMaker and S3 access. You will see instructions to use this role in the `provider.yaml` below.

3. (5 minutes) Data Upload - SageMaker relies on S3 as the primary data source for inputs and outputs of each job. Create a S3 bucket in the same region you plan to run jobs in and upload in the files from the `/data` folder of this tutorial. The name of the bucket should contain the keyword `sagemaker`, in order for the Sagemaker role above to have access to the bucket.

4. (3 minutes) Create a ECR Repo - Follow the [AWS instructions on creating an ECR repo](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html) and create an ECR repo, keeping the region consistent with the region in which the S3 bucket was created.

5. (2 minutes) Docker - Have [docker desktop](https://docs.docker.com/desktop/) or [Docker Engine](https://docs.docker.com/engine/) installed on your local machine. If you are on Linux, you may want to [run docker as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/).

## Usage

1. Installation

Install the latest `dev` version of `mlctl`. The latest releases are available on [PyPi](https://pypi.org/project/mlctl/#history):

    ```
    pip install mlctl==0.0.6.dev1
    ```

2. Point mlctl to your infrastructure

Edit the `provider.yaml`:

- Replace `iam_arn_for_running_jobs` with your ARN role from the Step 2 prereqs.
- Replace the `container_repo_on_ECR` with the repo created in Step 4 of the prereqs. 

The `provider.yaml` file below is an example of how the final file should look. Our ECR repo is in us-east-1, but you could use another region.

    ```
    mlctl_version: 0.1
    infrastructure:
    - name: awssagemaker
      arn: arn:aws:iam::123456789:role/sagemaker-execution-role
      container_repo: 123456789.dkr.ecr.us-east-1.amazonaws.com/ecr-repo-for-sagemaker
    resources: 
      process: 'ml.t3.medium'
      train: 'ml.m5.large'
      deploy: 'ml.t2.medium'
    ```

### Processing Job

1. Build the process job

Most models require data processing before it can be used. You can inspect the data processing code by navigating to `sklearn_tree/process.py`. The mapping of all the other job starting points can be found in `setup.py` entry_points. Mlctl is taking your code as an entrypoint and running bootstrap and post-job code that is required by the underlying MLOps infrastructure.

The code needs to be compiled to a container, which mlctl does automatically for you with a runtime utility called mlsriracha. To start the process, run the following commands to build each job:

    ```
    mlctl process build -c process.yaml
    
    ```

2. Upload process job container to ECR

ECR has a custom login script. To start that command, run `aws ecr get-login-password`. If you need to specify an AWS region, [read through the command options](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html#cli-authenticate-registry) in full.

Once the above command successfully retrieves the credentials, use these commands to upload the docker image to ECR:

    ```
    aws ecr get-login-password | docker login --username AWS --password-stdin <ecr URL>
    docker tag process-image <ecr URL>:process-image
    docker push <ecr URL>:process-image
    ```

3. Define and run the process job

The process job takes a file, and then does simple filtering, and saves it back in another S3 directory. Edit the `process.yaml` with the S3 bucket you uploaded the Step 3 prereq above. The output can be a different folder in the same S3 bucket. `mlctl` defines jobs by project, job name, data files, and inputs. For process jobs, typically the user inputs are minimal and the only parameter to change is the data source.

```
mlctl_version: 0.1
metadata:
  version: 1.0
  project: weight_data_aws
  job_type: process
data:
  input: s3://mlctltest/example1_data/train
  output: s3://mlctltest/example1_data_out/
```
After the `process.yaml` has been changed, the process job can be run

    ```
    mlctl process start -c process.yaml
    ```

### Training Job

1. Build, upload, and run the Train job

The training job requires a similar compilation step. Replace the 

    ```
    mlctl train build -c train.yaml
    docker tag train-image 123456789.dkr.ecr.us-east-1.amazonaws.com/ecr-repo-for-sagemaker:train-image
    docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/ecr-repo-for-sagemaker:train-image
    ```

The training job yaml in `train.yaml` requires the data inputs and outputs be updated with your S3 bucket. 

### Deploy the model for online inference

1. Build, upload, and create a model endpoint
    ```
    docker tag deploy-image 123456789.dkr.ecr.us-east-1.amazonaws.com/ecr-repo-for-sagemaker:deploy-image
    docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/ecr-repo-for-sagemaker:deploy-image
    mlctl deploy build -c deploy.yaml
    ```

    This will host the prediction function on your local machine
    identically to how it would be hosted in sagemaker.

2. Test the endpoint

Find the name of the endpoint by checking the logs. The patterns is XXXXXXXXX, and replace the `endpoint_name_value` below with the SageMaker provided endpoint name.

```
aws sagemaker invoke-endpoint
--endpoint-name <endpoint_name_value>
--body {"instances":[{"age": 35, "height": 182}]}
```