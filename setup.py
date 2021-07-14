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
    packages=["mlctl", "baklava"],
    include_package_data=True,

    # Insert dependencies list here
    install_requires=[
        'requests',
        'deprecation',
        'cachetools',
        'click',
        'boto3',
        'cookiecutter',
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
