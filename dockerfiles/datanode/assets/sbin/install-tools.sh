#!/usr/bin/env bash

set -e

echo "[INFO] Installing tools" && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        dialog \
        apt-transport-https \
        apt-utils \
        zip \
        unzip \
        python-pip \
        jq \
        openssh-server \
        gnupg2

echo "[INFO] Installing python libraries" && \
    # pip install --upgrade pip && \
    pip install \
        requests



