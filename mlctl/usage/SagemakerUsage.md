# **Sagemaker**

## **Prerequisites**

`mlctl` assumes that AWS credentials have been configured in the following locations (listed in search order)
1. [Environment variables](https://docs.aws.amazon.com/sdk-for-php/v3/developer-guide/guide_credentials_environment.html)
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY  
AWS_SESSION_TOKEN (needed only if using temporary credentials)
```
2. [Shared config and credential files](https://docs.aws.amazon.com/sdkref/latest/guide/creds-config-files.html)
```
~/.aws/credentials
~/.aws/config
```

AWS credential profile and `mlctl` plugin can be exported as environment variables or passed in as command line options. 

1. Environment variables: 

    ```
    export PLUGIN=sagemaker
    export PROFILE=preprod
    ```

2. Command line options:

    ```
    -pl sagemaker
    -pr preprod
    ```
`Note`: The values passed as command line options will be used if both are provided. 

## **Training Example**

### **Train a Model**
---
Create a JSON file storing parameters needed to make calls to the Amazon Sagemaker [CreateTrainingJob](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateTrainingJob.html) or [CreateHyperParameterTuningJob](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateHyperParameterTuningJob.html) APIs and pass the file as a command line option: `-c / --config`. 

Without hyperparameter tuning: 
```
mlctl train start -c training_config.json
```

With hyperparameter tuning: 
```
mlctl train start -c training_config.json --hyperparameter-tuning
```

### **Stop a Training Job**
---
Without hyperparameter tuning: 
```
mlctl train stop -t training-job-name
```
With hyperparameter tuning: 
```
mlctl train stop -t training-job-name --hyperparameter-tuning
```
### **Get Training Job Information**
---
Without hyperparameter tuning: 
```
mlctl train info -t training-job-name
```
With hyperparameter tuning: 
```
mlctl train info -t training-job-name --hyperparameter-tuning
```

## **Hosting Example**

### **Create a Sagemaker Model**
---
Create a JSON file storing parameters needed to make calls to the Amazon Sagemaker [CreateModel](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateModel.html) API and pass the file as a command line option: `-c / --config`. 
```
mlctl hosting create -c model_config.json
```

### **Deploy a Model**
---
If you do not have an existing endpoint config, create a JSON file storing parameters needed to make calls to the Amazon Sagemaker [CreateEndpointConfig](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateEndpointConfig.html) API and pass the file as a command line option: ` -c / --endpoint-config`. 

Without an existing endpoint config: 
```
mlctl hosting deploy -e endpoint-name -c endpoint_config.json 
```

With an existing endpoint config: 
```
mlctl hosting deploy -e endpoint-name -ec endpoint-config-name
```
`Note`: Please only pass either an endpoint file OR the name of an existing endpoint config. 

### **Undeploy a Model**
---
`mlctl` provides the ability to delete the endpoint config used to deploy a model when undeploying a model. 

Undeploy a model: 
```
mlctl hosting undeploy -e endpoint-name
```

Undeploy a model and delete corresponding endpoint config: 
```
mlctl hosting undeploy -e endpoint-name -c endpoint-config-name
```

### **Get Endpoint Info**
---
```
mlctl hosting info -e endpoint-name
```

## **Batch Inference Example**

### **Perform Batch Inference**
---
Create a JSON file storing parameters needed to make calls to the Amazon Sagemaker [CreateTransformJob](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateTransformJob.html) API and pass the file as a command line option: `-c / --config`. 

```
mlctl batch start -c batch_config.json 
```

### **Stop Batch Inference Job**
---
```
mlctl batch stop -b batch-job-name 
```

### **Get Batch Inference Job Information**
---
```
mlctl batch info -b batch-job-name
```

