#!/usr/bin/env bash

set -e

echo "[INFO] Cleaning" && \
    apt-get clean -y && \
    apt-get autoremove -y && \
    apt-get autoclean -y
