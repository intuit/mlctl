# ------------------------------------------------------------------------------
# Host
# ====
# The container which hosts the python function using nginx and lambda-server
# ------------------------------------------------------------------------------

FROM python:$python_version-slim

# Install server dependencies and setup permissions
RUN apt-get -y update \
 && apt-get install -y --no-install-recommends build-essential nginx \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir flask==1.1.2 gunicorn==20.0.4 gevent==20.9.0 psutil==5.7.2 six==1.15.0

# Copy static artifacts
COPY nginx.conf /opt/nginx.conf

# Define image entry
ENTRYPOINT ["python", "/opt/main.py"]

# Set up environment
ENV PYTHONUNBUFFERED=TRUE \
    PYTHONDONTWRITEBYTECODE=TRUE \
    LAMBDA_SERVER_WORKERS="$workers" \
    PIP_INDEX_URL="$pip_index_url" \
    PIP_TRUSTED_HOST="$pip_trusted_host" \
    PIP_EXTRA_INDEX_URL="$pip_extra_index_url"

# Insert custom docker lines (Do before pip installs for system dependencies)
$dockerlines

# Install any package-specific python requirements
$requirements

# Copy over entrypoint script and define image entry
COPY main.py /opt/main.py

# Copy and install prediction code
COPY $distribution /opt/$distribution
RUN pip install /opt/$distribution
