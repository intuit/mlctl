from setuptools import setup, find_packages

setup(
    name='{{ cookiecutter.package_name.lower().replace(' ', '_').replace('-', '_') }}',
    version='0.1.0',
    description="{{ cookiecutter.description }}",
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