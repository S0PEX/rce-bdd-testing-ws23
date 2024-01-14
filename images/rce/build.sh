#!/bin/bash

VERSION=latest
RCE_VERSION=10.5.0

# Build the image
docker build \
  --build-arg VERSION=$VERSION \
  --build-arg RCE_VERSION=$RCE_VERSION \
  --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
  -t "s0pex/rce-$RCE_VERSION:$VERSION" .
