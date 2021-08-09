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
    dockerlines=[],
    python_version='3.6',
    entry_points={
        'mlbaklava.process': [
            'my_process_entrypoint = sklearn_tree.process:main',
        ],
        'mlbaklava.train': [
            'my_train_entrypoint = sklearn_tree.train:main',
        ],
        'mlbaklava.deploy': [
            'my_prediction_entrypoint = sklearn_tree.deploy:main',
        ]
    }
)
