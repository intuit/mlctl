from setuptools import setup, find_packages

setup(
    name='sample_project',
    version='0.1.0',
    description="Python Boilerplate ML model contains all the boilerplate you need to create a working ML model project.",
    packages=find_packages(),
    install_requires=[
            'mlsriracha>=0.0.2'
        ],
    python_requires='>=3.6',
    entry_points={
        'mlbaklava.train': [
            'example_train = model.train:train'
        ],
        'mlbaklava.predict': [
            'example_predict = model.predict:predict',
        ],
    },
)