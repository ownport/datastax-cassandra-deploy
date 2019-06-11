#!/usr/bin/env bash

set -e

echo "[INFO] Installing OpenJDK 8" && \
    DEBIAN_FRONTEND="noninteractive" \
        apt-get install -y --no-install-recommends \
            openjdk-8-jdk && \
    java -version
