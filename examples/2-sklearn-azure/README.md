Sklearn Tree for Azure ML
============

This takes the 1-sklearn-tree-aws example project, but adapts it to Azure ML. The second example is designed to show how zero code changes are made, and the adaptions are entirely through config YAML files. 

Prereqs.
-----

1. (3 minutes) Install Azure 2.0 CLI. Azure has (instructions on how to install the CLI)[https://docs.microsoft.com/en-us/cli/azure/install-azure-cli] depending on your OS version. After, authenticate to Azure using the `az login` command or by providing your service principal.

2. (5 minutes) Create an Azure Machine Learning workspace and Studio Cluster - Visit the (machine learning product in the Azure console)[https://portal.azure.com/#create/Microsoft.MachineLearningServices]. Creating a new workspace will include a new a container registry and storage account that can be used for uploading containers and placing data. 

3. (2 minutes) Data Upload - Upload the data folder of this tutorial into the Azure bucket. 

4. (3 minutes) Create an Azure ML compute cluster. Users can create a compute environment within the Azure ML studio by navigating to `New > Training cluster` in the side bar. Alternatively, users can (create a cluster by using the SDK)[https://docs.microsoft.com/en-us/azure/machine-learning/how-to-create-attach-compute-cluster?tabs=python]. We use a cluster opposed to a compute instance because a cluster can autoscale from zero without a schedule.

6. (2 minutes) Docker - Have docker desktop or Docker CLI on your local machine.

Usage
-----

1. Installation. 

Install the latest release of mlctl. This will also install mlbaklava, the packaging library used to build container jobs with your Python code. 

    ```
    pip install mlctl
    ```

2. Point mlctl to your infrastructure. 

Edit the `provider.yaml`. Replace `iam_arn_for_running_jobs` with your ARN role from the Step 2 prereqs. Replace the `container_repo_on_ECR` with the repo created in Step 4 of the prereqs. The `provider.yaml` file is an example of how the final should look. Our ECR repo is in us-east-1, but you could use another region.

    ```
    mlctl_version: 0.1
    infrastructure:
      name: azureml
      container_repo: mlctl.azurecr.io/mlctl/myrepo
      resource_group: mlctl
      workspace_name: mlctl-test
    resources: 
      deploy: Standard_DS2_v2
    ```

3. Build the train job. 

Most models require data processing before it can be used. You can inspect the data processing code by navigating to `sklearn_tree/process.py`. The mapping of all the other job starting points can be found in `setup.py` entry_points. Mlctl is taking your code as an entrypoint and running bootstrap and post-job code that is required by the underlying MLOps infrastructure.

The code needs to be compiled to a container, which mlctl does automatically for you with a runtime utility called mlsriracha. To start the process, run the follow commands to build each jobs

    ```
    mlctl train build -c train.yaml
    
    ```

4. Upload train job container to ACR

ACR has a custom login script. To start that command, run `az acr login`. If you need to specify an Azure ACR command, [read through the options](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-authentication?tabs=azure-cli) in full.

    ```
    docker tag train-image <myregistry>.azurecr.io/<myregistry>/<myrepo>:train-image
    docker push <myregistry>.azurecr.io/<myregistry>/<myrepo>:train-image
    ```

5. Define and run the train job

The train job takes a file trains a decision tree model, and outputs the model back to the local directory. Edit the `train.yaml` with the (Azure Blob URI)[https://docs.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#resource-uri-syntax] you uploaded the Step 3 prereq above. Mlctl defines jobs by project, job name, data files, and inputs. For process jobs, typically the user inputs are minimal and the changed parameter is the data source.

```
mlctl_version: 0.1
metadata:
  version: 1.0
  project: height_data
  job_name: sklearndemo
  job_type: train
env_vars:
  hp_eta: 0.3
  hp_max_depth: 3
  hp_objective: multi:softprob
  hp_num_class: 3
data:
  input: https://mlctldata.blob.core.windows.net/modeldata/data.csv
```

After the `train.yaml` has been changed, the train job can be run

    ```
    mlctl train start -c train.yaml
    ```

6. Build, upload, and run the deploy job

The deploy job requires a similar compilation step. Run the similar compilation and upload step to ACR.

    ```
    mlctl deploy build -c deploy.yaml
    docker tag deploy-image <myregistry>.azurecr.io/<myregistry>/<myrepo>:deploy-image
    docker push <myregistry>.azurecr.io/<myregistry>/<myrepo>:deploy-image
    ```

After, modify the deployment job file to include the location for the model artifact. 

Note: Azure separates the model endpoint resources from any existing instance in the training cluster. 

    ```
    mlctl_version: 0.1
    metadata:
      name: my-new-endpoint
      job_type: deploy
      project: height_data
    resources: Standard_DS2_v2
    models:
      - name: sklearn-model1
        artifact: https://<storage_account_address>.blob.core.windows.net/<folder>/model.pkl
        version: 1
    ```

8. Test the endpoint

Within the Azure ML studio, look for the "Endpoints" tab. There will be a test endpoint modal where you can copy the inference request to submit. Copy the JSON request query below

```
{"instances":[{"age": 35, "height": 182}]}
```