# ------------------------------------------------------------------------------
# Execute
# =======
# Defines the base image for all regular executions (such as training jobs)
# ------------------------------------------------------------------------------

FROM python:$python_version-slim

# Define image entry
ENTRYPOINT ["python", "/opt/main.py"]

# Set up environment
ENV PIP_INDEX_URL="$pip_index_url" \
    PIP_TRUSTED_HOST="$pip_trusted_host" \
    PIP_EXTRA_INDEX_URL="$pip_extra_index_url"

# Insert custom docker lines (Do before pip installs for system dependencies)
$dockerlines

# Install any package-specific python requirements
$requirements

# Copy entrypoint script
COPY main.py /opt/main.py

# Copy and install training code
COPY $distribution /opt/$distribution
RUN pip install /opt/$distribution
