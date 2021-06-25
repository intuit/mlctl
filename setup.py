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
    packages=find_packages(),
    include_package_data=True,

    # Insert dependencies list here
    install_requires=[
        'requests',
        'deprecation',
        'cachetools'
    ],

    maintainer='Intuit ML Platform',
    maintainer_email='mlctl-maintainers@intuit.com',
    url='https://github.com/intuit/mlctl',

    entry_points={
        'console_scripts': [
            'mlctl = mlctl.clis.cli:_mlctl_pass_through'
        ]
    }
)
