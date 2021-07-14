"""
Images
======
Utility functions for building and running docker images
"""
import os
import hashlib
import tarfile
import six
import re

from distutils import log
import docker
from docker.errors import ImageNotFound, BuildError
from docker.utils.json_stream import json_stream


# ------------------------------------------------------------------------------
# Generic Operations
# ------------------------------------------------------------------------------

def check_docker():
    """
    Check that docker is actually running.

    Returns:
        status (bool): Whether or not docker is running.
    """
    try:
        import docker
        client = docker.from_env()
        client.ping()
        return True
    except:
        log.error('Docker is not running. Please open or install it.')
        return False


def build(directory, name):
    """
    Build an image using a Dockerfile at a specific path using the full name to
    tag the resulting image.

    Arguments:
        directory (str): The directory containing the Dockerfile for the
            distribution.
        name (str): The full name of the resulting image including
            the repository and tag of the image.
        buildargs (dict[str, str]): A set of arguments to pass the build
            command. These will be set as environment variables in the resulting
            image.
    """

    # Load docker client
    client = docker.from_env()

    # Attempt to find image if it exists
    try:
        client = docker.from_env()
        image = client.images.get(name)
        log.info('found image: {}'.format(name))
        return image
    except ImageNotFound:
        pass

    # Build image if it doesn't exist
    log.info('building image: {}'.format(name))
    resp = client.api.build(
        path=directory,
        tag=name,
        quiet=False,
    )

    if isinstance(resp, six.string_types):
        return client.images.get(resp)

    last_event = None
    image_id = None

    # Parse and log build stream
    for chunk in json_stream(resp):
        if 'error' in chunk:
            raise BuildError(chunk['error'], '')
        if 'stream' in chunk:
            match = re.search(
                r'(^Successfully built |sha256:)([0-9a-f]+)$',
                chunk['stream']
            )
            if match:
                image_id = match.group(2)

            formatted = chunk['stream'].rstrip()
            if formatted:
                log.info(formatted)
        last_event = chunk

    # If stream produced an image id, fetch the image
    if image_id:
        return client.images.get(image_id)

    # If no image id was produced we have an error
    raise BuildError(last_event or 'Unknown', '')


def rename(name, new):
    """
    Retags an image with a given full name to the new name.

    Arguments:
        name (str): The existing name of the image.
        new (str): The new name of the image.
    """
    client = docker.APIClient()
    client.tag(name, new)
    log.info('tagged: {}'.format(new))


def md5(artifacts):
    """
    Get the MD5 checksum for the distribution artifacts. This ignores the
    timestamp generally included in the distribution archive to be able to
    reproduce checksums solely based off of file content

    Arguments:
        artifacts (list[str]): The list of all model artifact files.

    Returns:
        checksum (str): The checksum of the tar file contents.
    """
    hash_md5 = hashlib.md5()

    for filename in artifacts:

        # Handle tar files
        if filename.endswith('tar.gz'):
            tar = tarfile.open(name=filename, mode="r:gz")
            for member in tar.getnames():
                content = tar.extractfile(member)
                if content:
                    hash_md5.update(content.read())
            continue

        # Don't hash directories
        if os.path.isdir(filename):
            continue

        # Handle all other files
        with open(filename, 'rb') as stream:
            hash_md5.update(stream.read())

    return hash_md5.hexdigest()


def tag(artifacts, name, version):
    """
    Creates a tag with the following naming convention:

        name:version-checksum

    For example:

        example:0.0.1-af873cebe8
        example:0.0.1-af873cebe8

    Note: The purpose of including an artifact checksum in the tag is so that
    an identical image can be looked up immediately without rebuilding the
    image. By default `.tar.gz` files include a timestamp of when the archive
    was created which means `sdist` files can never be cached unless manually
    looking at the contents (i.e. the `images.md5` routine)

    Arguments:
        artifacts (list[str]): The locations of the distribution artifacts
        name (str): The name of the distribution
        version (str): The version of the distribution

    Returns:
        str: The tag string
    """
    checksum = md5(artifacts)
    docker_tag = '{}-{}'.format(version, checksum)

    # Here we remove random punctuation to be compliant with docker tagging.
    # This scenario will occur when using `setuptools-scm` in development
    docker_tag = re.sub(r"[^\w.-]", '.', docker_tag)

    return '{}:{}'.format(name, docker_tag)
