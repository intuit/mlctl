# **[mlctl](https://github.com/intuit/mlctl)**

![mlctl logo](.github/assets/images/mlctl-logo.png)

`mlctl` is the Command Line Interface (CLI)/Software Development Kit (SDK) for MLOps. It allows for all ML Lifecycle operations, such as `Training`, `Deployment` etc. to be controlled via a simple-to-use command line interface. Additionally, `mlctl` provides a SDK for use in a notebook environment and employs an extensible mechanism for plugging in various back-end providers, such as SageMaker. 

The following ML Lifecycle operations are currently supported via `mlctl`
- `train` - operations related to model training
- `host` - operations related to hosting a model for online inference 
- `batch inference` - operations for running model inference in a batch method

# **Getting Started**

## **Installation** 

1. (*Optional*) Create a new virtual environment for `mlctl`

    ```
    pip install virtualenv
    virtualenv ~/envs/mlctl
    source ~/envs/mlctl/bin/activate
    ```
    
2. Install `mlctl`:

    ```
    pip install mlctl
    ```

3. Upgrade an existing version:
    
    ```
    pip install --upgrade mlctl
    ```
# **Usage**
## **Optional Setup**
`mlctl` requires users to specify the plugin and a profile/credentials file for authenticating operations. These values can either be stored as environment variables as shown below OR they can be passed as command line options. Use `--help` for more details.
    
    ```
    export PLUGIN=
    export PROFILE=
    ```
## **Commands**
`mlctl` CLI commands have the following structure:
```
mlctl <command> <subcommand> [OPTIONS]
```

To view help documentation, run the following: 
```
mlctl --help
mlctl <command> --help
mlctl <command> <subcommand> --help
```

### **Training Commands**
---

```
mlctl train <subcommand> [OPTIONS]
```
| Subcommand | Description
| -----------|-------------  
| start      | train a model 
| stop       | stop an ongoing training job  
| info       | get training job information

### **Hosting Commands**
---
```
mlctl hosting <subcommand> [OPTIONS]
```
| Subcommand | Description
| -----------|-------------  
| create     | create a model from trained model artifact
| deploy     | deploy a model to create an endpoint for inference
| undeploy   | undeploy a model
| info       | get endpoint information

### **Batch Inference Commands**
---
```
mlctl batch <subcommand> [OPTIONS]
```
| Subcommand | Description
| -----------|-------------  
| start      | perform batch inference
| stop       | stop an ongoing batch inference 
| info       | get batch inference information

# **Examples**
* **[Sagemaker](./mlctl/usage/SagemakerUsage.md)**

# **Contributing**
For information on how to contribute to `mlctl`, please read through the [contributing guidelines](./.github/CONTRIBUTING.md).

