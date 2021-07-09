from setuptools import setup, find_packages

setup(
    name='{{ cookiecutter.project_slug }}',
    version='{{ cookiecutter.version }}',
    description="{{ cookiecutter.project_short_description }}",
    packages=find_packages(),
    install_requires=[
        'tensorflow==1.13.1',
        'pandas==0.24.2',
        'featurizer>=0.0.29',
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