from setuptools import setup, find_packages

setup(
    name='{{ cookiecutter.project_slug }}',
    version='{{ cookiecutter.version }}',
    description="{{ cookiecutter.project_short_description }}",
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