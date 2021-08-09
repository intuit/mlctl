from setuptools import setup, find_packages

setup(
    name='sklearn_tree',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'sklearn',
        'pandas',
        'scipy',
    ],
    dockerlines=[
        'COPY mlsriracha /opt/mlsriracha',
        'RUN cd /opt/mlsriracha && pip install .',
    ],
    python_version='3.6',
    entry_points={
        'baklava.train': [
            'my_training_entrypoint = sklearn_tree.train:main',
        ],
        'baklava.predict': [
            'my_prediction_entrypoint = sklearn_tree.predict:main',
        ]
    }
)
