from setuptools import setup, find_packages

setup(
    name='{{ cookiecutter.package_name.lower().replace(' ', '_').replace('-', '_') }}',
    version='0.1.0',
    description="{{ cookiecutter.description }}",
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