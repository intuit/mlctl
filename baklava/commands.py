"""
Commands
========
Setuptools entrypoints for building training/prediction docker containers from
distributions.
"""

from distutils.core import Command
import os


from baklava import images, entrypoint, distribution


class Docker(Command):

    def build(self, artifacts, entry, directory):
        # Exit if we do not want to build
        if self.nobuild:
            return

        # Check for docker before building
        if not images.check_docker():
            return

        # Extract distribution parameters for building
        name = self.distribution.metadata.name
        version = self.distribution.metadata.version

        # Come up with name and tag for the resulting image
        if self.entrypoint is not None:
            entry_name, entry_package, entry_func = entry
            name = '{}-{}'.format(name, entry_name)
        tag = images.tag(artifacts, name, version)

        # Build and tag the image
        image = images.build(directory, name=tag)

        # Save the identity file if a name is provided
        if self.idfile:
            with open(self.idfile, 'w') as stream:
                stream.write(image.id)

        if self.tag is not None:
            images.rename(image.id, self.tag)

        if self.hash:
            print(image.id)


class Train(Docker):
    description = 'create a docker image for local training'
    user_options = [

        # Distribution Configs
        ('entrypoint=', 'e', "The project entrypoint"),

        # Docker Configs
        ('idfile=', 'f', "Save image name to the given file"),
        ('tag=', 't', "Tag the image with a string"),

        # Flags
        ('nobuild', 'b', "Flag to not build the image"),
        ('hash', 'h', "Silently build and output image hash"),
    ]

    def initialize_options(self):

        # Distribution Configs
        self.entrypoint = None
        self.pyver = None

        # Docker Configs
        self.idfile = None
        self.tag = None

        # Flags
        self.nobuild = False
        self.hash = False

    def finalize_options(self):
        pass

    def run(self):

        # Get the entrypoint
        entry = entrypoint.get(
            entry=self.distribution.entry_points,
            key='baklava.train',
            name=self.entrypoint
        )

        # Create the source distribution
        self.run_command('sdist')
        sdist = self.get_finalized_command('sdist')
        assert len(sdist.archive_files), RuntimeError(
            'Expected a single archive to be created from source distribution'
        )

        # Extract path to the distribution
        path = sdist.archive_files[0]
        directory = sdist.dist_dir
        archive = os.path.relpath(path, directory)

        # Extract distribution configurations
        requirements = self.distribution.install_requires
        python_version = self.distribution.python_version
        dockerlines = self.distribution.dockerlines

        # Build docker distribution files
        artifacts = distribution.train(
            path=directory,
            archive=archive,
            entrypoint=entry,
            requirements=requirements,
            python_version=python_version,
            dockerlines=dockerlines
        )

        self.build(artifacts, entry, directory)


class Predict(Docker):
    description = 'create a docker image for local prediction'
    user_options = [

        # Distribution Configs
        ('entrypoint=', 'e', "The project entrypoint"),
        ('initializer=', 'n', "The project initializer"),
        ('workers=', 'e', "The number of worker processes host in the image (default=8)"),

        # Image Configs
        ('idfile=', 'f', "Save image name to the given file"),
        ('tag=', 't', "Tag the image with a string"),

        # Flags
        ('nobuild', 'b', "Flag to not build the image"),
        ('hash', 'h', "Silently build and output image hash"),
    ]

    def initialize_options(self):

        # Distribution Configs
        self.entrypoint = None
        self.initializer = None
        self.workers = None

        # Docker Configs
        self.idfile = None
        self.tag = None

        # Flags
        self.nobuild = False
        self.hash = False

    def finalize_options(self):
        pass

    def run(self):

        # Get the initializer
        initializer = (None, None, None)
        if self.initializer or 'baklava.initialize' in self.distribution.entry_points:
            initializer = entrypoint.get(
                entry=self.distribution.entry_points,
                key='baklava.initialize',
                name=self.initializer
            )

        # Get the entrypoint
        entry = entrypoint.get(
            entry=self.distribution.entry_points,
            key='baklava.predict',
            name=self.entrypoint
        )

        # Create the source distribution
        self.run_command('sdist')
        sdist = self.get_finalized_command('sdist')
        assert len(sdist.archive_files), RuntimeError(
            'Expected a single archive to be created from source distribution'
        )

        # Extract path to the distribution
        path = sdist.archive_files[0]
        directory = sdist.dist_dir
        archive = os.path.relpath(path, directory)

        # Extract distribution configurations
        requirements = self.distribution.install_requires
        python_version = self.distribution.python_version
        dockerlines = self.distribution.dockerlines

        # Build docker distribution files
        artifacts = distribution.predict(
            path=directory,
            archive=archive,
            entrypoint=entry,
            requirements=requirements,
            initializer=initializer,
            python_version=python_version,
            dockerlines=dockerlines,
            workers=self.workers
        )

        self.build(artifacts, entry, directory)


def passthrough(dist, keyword, value):
    """
    This function is used to register distutils keywords
    """
    pass
