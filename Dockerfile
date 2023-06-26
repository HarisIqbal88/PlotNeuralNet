# The Linux distro install instructions from https://miktex.org/download are used here.
# This Dockerfile creates a docker container that has all necessary packages installed to create the NN diagrams
# Remember, if needed to rebuild, look at the README for cmd line instructions
#
# Authors: [Christopher Endres (cmendres400@gmail.com)]
# Date Created: 06/26/2023
# Last Updated: 06/26/2023
# Version: 1.0

### Stage 1, use Ubuntu 20.04 as base image ###
FROM ubuntu:20.04 AS base

# Set home directory
ENV HOME=/home/pnn
WORKDIR $HOME

# Set user to root
USER root

# Set env name
ARG ENV_NAME=pnn
	
# Update and install dependencies for python3.10 install
RUN apt-get update -y && \
	apt-get install software-properties-common -y && \
	add-apt-repository ppa:deadsnakes/ppa

# Install python3.10 and other dependencies
RUN apt-get install python3.10 -y && \
	apt-get install -y python3-distutils python3-pip python3-apt

# Remove python3 virtualenv, install virtualenv
RUN apt-get remove -y python3-virtualenv && \
	pip install --user virtualenv --force-reinstall 

# Add the 'tree' command for debugging
RUN apt-get update && \
	apt-get install -y tree


### Stage 2, install miktex ###
# All credits to this stage go to Christian Schenk, contents can be found at https://github.com/MiKTeX/docker-miktex/blob/master/Dockerfile
FROM base AS miktex

# Install dependencies for miktex
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
		apt-transport-https \
		ca-certificates \
		dirmngr \
		ghostscript \
		gnupg \
		gosu \
		make \
		perl

# Download mixtex from source
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D6BC243565B2087BC3F897C9277A7293F59E4889
RUN echo "deb http://miktex.org/download/ubuntu focal universe" | tee /etc/apt/sources.list.d/miktex.list

# Install miktex
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        miktex

# Setup miktex
RUN miktexsetup finish && \
    initexmf --admin --set-config-value=[MPM]AutoInstall=1 && \
    mpm --admin \
		--install amsfonts \
		--install biber-linux-x86_64 && \
    initexmf --admin --update-fndb

### Stage 3, setup python venv and install poetry dependencies ###
FROM miktex AS env_setup

# Set Python/pip/Poetry ENV settings
ENV YOUR_ENV=${ENV_NAME} \
  	PYTHONFAULTHANDLER=1 \
  	PYTHONUNBUFFERED=1 \
  	PYTHONHASHSEED=random \
  	PIP_NO_CACHE_DIR=off \
  	PIP_DISABLE_PIP_VERSION_CHECK=on \
  	PIP_DEFAULT_TIMEOUT=100 \
  	PSUTILS_VERSION=5.9.4 \
  	POETRY_VERSION=1.4.1 \
	PIP_VERSION=22.3.1

# Install Poetry ans psutil, upgrade requests
RUN pip install --upgrade --user requests && \
	pip install --user "psutil==$PSUTILS_VERSION" && \
	pip install --user "poetry==$POETRY_VERSION" && \
	pip install --user "pip==$PIP_VERSION"

# Set project app workspace in linux distro
ENV WORK_DIR=$HOME/app

# Copy the poetry lock and pyproject toml file to the Dockerfile working dir (assuming the lock and toml files are in same dir as Dockerfile)
WORKDIR $WORK_DIR
# COPY poetry.lock $WORK_DIR/poetry.lock
# COPY pyproject.toml $WORK_DIR/pyproject.toml

# Copy the project files to the Dockerfile working dir (assuming the project files are in same dir as Dockerfile)
COPY . $WORK_DIR

# Set Poetry and Venv paths
ENV POETRY_PATH=$HOME/.poetry/bin/poetry \
  	VENV_PATH=$HOME/.local/bin/venv \
	BIN_PATH=$HOME/.local/bin/

# Add poetry, venv, and bin to path
ENV PATH="$POETRY_PATH:$VENV_PATH:$BIN_PATH:$PATH"

# Create virtual env
RUN poetry config virtualenvs.create true && \
	poetry config virtualenvs.options.system-site-packages true

# Install Poetry dependencies from lock file via requirements.txt file rather than poetry install (sometimes poetry install breaks from depreciated pip install)
RUN poetry export --without-hashes --with dev --format=requirements.txt > requirements.txt && \
	pip install --user -r requirements.txt && \
	rm requirements.txt
