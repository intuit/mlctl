from setuptools import setup, find_packages

setup(
    name='sample',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'baklava.train': [
            'train = sample.main:train',
        ],
        'baklava.predict': [
            'predict = sample.main:predict',
        ]
    }
)
