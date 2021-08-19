Sklearn Tree for Azure ML
============

This takes the 1-sklearn-tree-aws example project, but adapts it to Kubernetes. This third example is designed to show how zero code changes are made, and the adaptions are entirely through config YAML files. 

Prereqs.
-----

1. (10 minutes) Set up a Kubernetes cluster. For a quick setup, we use (Bitnami Kubernetes Sandbox)[https://aws.amazon.com/marketplace/pp/prodview-hy5b54ebhfcsm] that is on the marketplace for major cloud providers, including AWS where we tested our demo. When your Kubernetes cluster is running, apply the kubeconfig to your client. Bitnami has (specific instructions)[https://docs.bitnami.com/aws/infrastructure/kubernetes-sandbox/configuration/configure-local-kubectl/] for the credentials of the Kubeconfig. 

2. (2 minutes) Data Upload - Upload the data folder of this tutorial into the S3 bucket.

3. (2 minutes) Set up Dockerhub - 

4. (2 minutes) Add AWS credentials to cluster - 

Instructions.
------

1. Create a provider YAML 

2. Create a job YAML

3.