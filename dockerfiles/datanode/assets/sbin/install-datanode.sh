#!/usr/bin/env bash

set -e

# =========================================
# 
# Main
#
echo "[INFO] Modify the aptitude repository source list file (/etc/apt/sources.list.d/datastax.sources.list)" && \
    echo "deb https://debian.datastax.com/enterprise stable main" | \
        tee -a /etc/apt/sources.list.d/datastax.sources.list

echo "[INFO] Add the DataStax repository key to your aptitude trusted keys" && \
    curl -L https://debian.datastax.com/debian/repo_key | apt-key add -

