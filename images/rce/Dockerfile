# Base image: ubuntu:22.04
FROM ubuntu:22.04

# Image metadata
ARG BUILD_DATE
ARG VERSION
ARG RCE_VERSION
LABEL build_version="Linuxserver.io version:- ${VERSION} Build-date:- ${BUILD_DATE}"
LABEL maintainer="Artur Komaristych <artur.komaristych@gmail.com>"

# Ensure system is up-to-date
RUN apt-get update && apt-get upgrade -y

# Install required packages
RUN apt-get install -y \
    openjdk-18-jre-headless:amd64

# Install RCE & cleanup .deb file
COPY rce-${RCE_VERSION}*-standard.x86_64.deb .
RUN apt-get install -y ./rce-${RCE_VERSION}*-standard.x86_64.deb

# Cleanup
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN rm -rf rce-*.x86_64.deb

# Create user and change to it
RUN useradd -m -s /bin/bash rce
USER rce

# Copy configuration file to default location
COPY --chown=rce:rce configuration.json /home/rce/.rce/default/configuration.json

# Entrypoint as RCE in headless mode, as otherwise it will fail to start without a display server
ENTRYPOINT ["rce", "--headless", "--upgrade-profile"]
