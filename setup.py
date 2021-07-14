from setuptools import setup, find_packages

setup(

    # Package information
    name="mlctl",
    use_scm_version={
        "local_scheme": "no-local-version",
        "write_to": "mlctl/__version.py",
        "write_to_template": "__version__ = \"{version}\"\n",
    },

    setup_requires=["setuptools-scm"],

    # Package data
    packages=find_packages(
        include = ['mlctl', 'baklava'],
    ),
    include_package_data=True,

    # Insert dependencies list here
    install_requires=[
        'requests==2.25.1',
        'deprecation==2.1.0',
        'cachetools==4.2.2',
        'click==8.0.1',
        'boto3==1.17.108',
        'cookiecutter==1.7.3',
        'docker>=2.0.0',   # Earliest with compatible `docker.from_env` API
        'appdirs>=1.4.0'  # First version compatible with current pip paths
    ],

    maintainer='Intuit ML Platform',
    maintainer_email='mlctl-maintainers@intuit.com',
    url='https://github.com/intuit/mlctl',

    entry_points={
        'console_scripts': [
            'mlctl = mlctl.clis.cli:_mlctl_pass_through'
        ],
        'distutils.commands': [
            'train = baklava.commands:Train',
            'execute = baklava.commands:Train',
            'predict = baklava.commands:Predict',
            'serve = baklava.commands:Predict',
        ],
        'distutils.setup_keywords': [
            'python_version = baklava.commands:passthrough',
            'dockerlines = baklava.commands:passthrough',
        ],

    }
)
