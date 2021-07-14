from setuptools import setup, find_packages

setup(
    name='boilerplate_ml_model',
    version='0.1.0',
    description="Python Boilerplate ML model contains all the boilerplate you need to create a working ML model project.",
    packages=find_packages(),
    install_requires=[
        'mlctl'
    ],
    python_requires='>=3.6',
    #dockerlines="ARG DOCKER_IMAGE_NAME=${paws.registry}/${paws.gitOrg}/${paws.modal_name}/service/${paws.modal_name}:${DOCKER_TAGS}",,
    entry_points={
        'baklava.train': [
            'example_train = model.train:train'
        ],
        'baklava.predict': [
            'example_predict = model.predict:predict',
        ],
    },
)