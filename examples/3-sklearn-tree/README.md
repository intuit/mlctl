Sklearn Tree
============

This is an example project which builds on the first two examples but
builds a real model using the `sklearn` package. The major difference
between the first two examples and this one is that this includes many
more dependencies in the `setup.py`

Usage
-----

1. Install the release version of setuptools docker according to the
    directions found [Here](https://github.com/intuit/baklava)

2. Clone the repository and go to the `examples/` directory:

    ```
    git clone git@github.com:data-science/baklava.git
    cd baklava/examples/3-sklearn-tree
    ```

3. Build and execute the example training image using:

    ```
    python setup.py train -t train-image
    ```
    ```
    docker run -entrypoint="python /opt/main.py --set training-data='https://mlctldata.blob.core.windows.net/modeldata/data.csv'" train-image
    ```

    <!-- Doesn't work easily because requires pip install code package -->
    Local Hosting w/o container
    python3 ./dist/main.py --set
    training-data=./data/train \
    sriracha_provider=azureml \


    Local Interactive Docker experience
    docker run -it \
    -v $(pwd)/data/train/:/opt/ml/input/data/training \
    -v $(pwd)/data/model/:/outputs \
    -e training-data=/opt/ml/input/data/training/data.csv \
    -e sriracha_provider=azureml \
    --entrypoint="/bin/bash" train-image 

    docker run      -v $(pwd)/data/train/:/opt/ml/input/data/training     -v $(pwd)/data/model/:/outputs  -v ~/.aws/credentials:/.aws/credentials -e AWS_SHARED_CREDENTIALS_FILE=/.aws/credentials   -e AZURE_ML_INPUT_training=/opt/ml/input/data/training/data.csv     -e sriracha_provider=azureml,mlflow -e sriracha_mlflow_tracking_uri=http://ec2-34-234-193-241.compute-1.amazonaws.com:5000 -e sriracha_run_name=adhoctest1 -e sriracha_experiment_name=adhoc train-image


    az ml job create -f train.yaml --web --resource-group mlctl --workspace-name mlctl-test


    This will generate a `model.pkl` file in the `data/model/` folder.

4. Build and execute the example prediction image using:

    ```
    python setup.py predict -t predict-image
    ```
    ```
    docker run                                           \
    -p 8080:8080                                         \
    -v $(pwd)/data/model/:/opt/ml/model/                 \
    -e AZUREML_MODEL_DIR=/opt/ml/model/ \
    -e sriracha_provider=azureml \
    predict-image
    ```

    This will host the prediction function on your local machine
    identically to how it would be hosted in sagemaker.

5. The status of whether or not the server is running can be tested by
   accessing the `ping` route. In another terminal, execute a `GET` request
   to the `ping` route using `curl`:

    ```
    curl                                        \
    --header "Content-Type: application/json"   \
    --request GET                               \
    http://localhost:8080/ping
    ```

    If everything was successful, the server should emit this JSON
    response:

    ```
    {"success": true}
    ```

    az ml endpoint create --name sklearnendpoint -f endpoint.yaml  --resource-group mlctl --workspace-name mlctl-test


6. The prediction function defined in the `setup.py` can be run by
   accessing the `invocations` route. In another terminal, execute
   a `POST` request to the `invocations` route using `curl`:

    ```
    curl                                        \
    --header "Content-Type: application/json"   \
    --request POST                              \
    --data '{"instances":[{"age": 35, "height": 182}]}'         \
    http://localhost:8080/invocations
    ```

    If everything was successful, the server should emit this JSON
    response:

    ```
    {"weight": 172}
    ```


AWS Container Build

docker run  \
    -v $(pwd)/data/train/:/opt/ml/input/data/training \
    -v $(pwd)/data/model/:/outputs \
    -e training-data=/opt/ml/input/data/training/data.csv \
    -e sriracha_provider=awssagemaker \
    train-image 