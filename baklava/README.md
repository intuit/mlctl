# **Baklava**
![baklava logo](../.github/assets/images/baklava-logo.png)

Baklava is a package for building python based Machine Learning models into docker images, that can be deployed directly into cloud environments. Currently, AWS Sagemaker is supported out of the box

Baklava is an extension to the standard python packaging utility `setuptools`. The 
official [python packaging guide](https://packaging.python.org/)
explains the basics of building python distributions in detail.

Baklava extends the existing behavior of building a setuptools source
distribution (`sdist`) by installing the built package artifact
(`*.tar.gz`) into a Docker image. After the python distribution has been
installed to the Docker image, it allows the user to configure the image
for the purposes of model training and prediction.

This name was chosen for the project because the dessert [baklava](https://en.wikipedia.org/wiki/Baklava) consists of small pieces and layers. Analogously, the `baklava` package put technologies together in form of many layers to create Docker images.

## Installation

Install [docker](https://www.docker.com/) and then install the package:

```
pip install baklava
```

## Features

Installing the `baklava` package automatically registers
extensions to `setuptools`. New features are added to build python
distributions into docker images.

When installed, this package allows you to use two new **setuptools
commands** (similar to `sdist` or `bdist_wheel`):

* `train`: Builds a training docker image for your package. A training 
  image (`python setup.py train`) executes a user-provided function 
  just once in order to produce a model artifact. This image conforms to the AWS 
  SageMaker training image API.
  
* `predict`: Builds a prediction docker image for your package. A prediction
   image (`python setup.py predict`) hosts the user-provided function in a web 
   application to be able to produce many decisions over time using a RESTful 
   service conforming to the AWS SageMaker prediction API.
  
* `execute`: Builds a batch execution docker image for your package. A batch execution 
  image (`python setup.py execute`) executes a user-provided batch function for prediction 
  on large amount of records.
  
  
### Production-grade Machine Learning API using Flask, Gunicorn, Nginx, and Docker

![Flask App](docs/flask.png)

New **setup keywords** are also registered with setuptools (similar to
`install_requires` or `entry_points`). These include:

* `python_version`: Specify the version of python to build the docker image for
* `dockerlines`: Add docker commands to your resulting `Dockerfile`

This package also defines a [Python API](baklava/api.py) to perform 
the same actions as the setuptools extension.

## Usage

### Train

To create a training image, your package must define a function that
takes no arguments and returns nothing. It can be named anything as long
as it is correctly referenced in the `setup.py` file.

```python
def my_training_function():
    """
    A training function takes no arguments and returns no results
    """
    pass
```

The `setup.py` must include a `baklava.train` entrypoint which
points to this function. The entrypoint is the full module path to the
defined python function. An example of a `setup.py` script with a valid
training entrypoint would  look like the following:

```python
from setuptools import setup, find_packages

setup(
    name='example',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'baklava.train': [
            'my_entrypoint = example.main:my_training_function',
        ],
    }
)
```

With this `setup.py`, a training docker image can be built:

```
python setup.py train
```

See the [examples](examples/) for full sample projects.

### Predict

To create a prediction image, your package must define a function
that takes one argument and returns one value. It can be named anything
as long as it is correctly referenced in the `setup.py` file.

```python
def my_hosted_function(payload):
    """
    A hosted function takes a dictionary input and returns a dictionary
    output.

    Arguments:
        payload (dict[str, object]): This is the payload was sent to
            the SageMaker server using a POST request to the
            `invocations` route.

    Returns:
        result (dict[str, object]): The output of the function is
            expected to be either a dictionary (like the function input)
            or a JSON string.
    """
    return {}
```

The `setup.py` must include a `baklava.predict` entrypoint
which points to this function. The entrypoint is the full module path to
the defined python function. An example of a `setup.py` script with a
valid prediction entrypoint would  look like the following:

```python
from setuptools import setup, find_packages

setup(
    name='example',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'baklava.predict': [
            'my_entrypoint = example.main:my_hosted_function',
        ]
    }
)
```

With this `setup.py`, a prediction docker image can be built:

```
python setup.py predict
```

See the [examples](examples/) for full sample projects.

### Predict Initialization

There are often cases when python code needs to execute prior to running
predictions. For example, it may take a long time to load a model
artifact into memory.

To add a prediction initializer, your package must define a function
that takes no arguments and may return anything. It can be named
anything as long as it is correctly referenced in the `setup.py` file.
The function is responsible for it's own caching, but it is recommended
to use caching function similar to `functools.lru_cache` to save the
function results in memory.

```python
import functools

@functools.lru_cache()
def my_init_function():
    """
    An initialization function takes no arguments and may return a
    result.

    Returns:
        data (object): Data necessary for prediction. Could be any type.
    """
    return 1, 2, 3
```

The `setup.py` must include a `baklava.initialize` entrypoint
which points to this function. The entrypoint is the full module path to
the defined python function. An example of a `setup.py` script with a
valid prediction initialization entrypoint would  look like the
following:

```python
from setuptools import setup, find_packages

setup(
    name='example',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,

    # Notice that we have an initializer AND a predict function
    entry_points={
        'baklava.predict': [
            'my_entrypoint = example.main:my_hosted_function',
        ]
        'baklava.initialize': [
            'my_initializer = example.main:my_init_function',
        ]
    }
)
```

With this `setup.py`, a prediction docker image can be built that will
initialize using the `my_init_function` initializer:

```
python setup.py predict
```

See the [examples](examples/) for full sample projects.

### Multiple Options

A package may include all of the previous entrypoints in a single image
if that package is responsible for both training and prediction. Like
the previous examples, all that is required is to add a set of
entrypoints to an existing `setup.py` script.

In addition, we can also fix the `python_version` and add custom
`dockerlines` to the final image

```python
from setuptools import setup, find_packages

setup(
    name='example',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,

    # This will force the python version for the resulting image
    python_version='3.6.6',

    # This will run during the docker build stage
    dockerlines=[
        'RUN echo Hello, World!',
        'RUN echo Hello, Sailor!',
    ],

    # The predict and train entrypoints create distinct images
    entry_points={
        'baklava.train': [
            'my_train_entrypoint = example.main:my_training_function',
        ],
        'baklava.predict': [
            'my_predict_entrypoint = example.main:my_hosted_function',
        ]
        'baklava.initialize': [
            'my_initializer = example.main:my_init_function',
        ]
    }
)
```

With this `setup.py`, both a prediction and a training docker image can
be built:

```
python setup.py predict
python setup.py train
```

# Community
Engage with the Baklava + MLCTL community on Slack at:

[https://mlctl.slack.com/](https://mlctl.slack.com/)

# Contributing
For information on how to contribute to `baklava`, please read through the [contributing guidelines](./.github/CONTRIBUTING.md).