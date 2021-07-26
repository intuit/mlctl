from setuptools import setup, find_packages

setup(
    name='sample_project',
    version='0.1.0',
    description="Python Boilerplate ML model contains all the boilerplate you need to create a working ML model project.",
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.6',
    entry_points={
        'baklava.train': [
            'example_train = model.train:train'
        ],
        'baklava.predict': [
            'example_predict = model.predict:predict',
        ],
    },
)