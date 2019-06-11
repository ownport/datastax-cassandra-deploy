#!/usr/bin/env bash

set -e

DATASTAX_OPSCENTER_VERSION="6.7.3"

# =========================================
# 
# Configure DataStax OpsCenter
#
configure_opscenter() {

    echo "[INFO] Backup default OpsCenter configuration file to /etc/opscenter/opscenterd.conf.bak" && \
        cp /etc/opscenter/opscenterd.conf /etc/opscenter/opscenterd.conf.bak 

    echo "[INFO] Turn on OpsCenter authentication" && \
        sed -i 's/enabled = False/enabled = True/g' /etc/opscenter/opscenterd.conf

    echo "[INFO] Turn on SSL for OpsCenter" && \
        sed -i 's/#ssl_keyfile/ssl_keyfile/g' /etc/opscenter/opscenterd.conf && \
        sed -i 's/#ssl_certfile/ssl_certfile/g' /etc/opscenter/opscenterd.conf && \
        sed -i 's/#ssl_port/ssl_port/g' /etc/opscenter/opscenterd.conf

    echo "[INFO] Turn on Agent SSL for OpsCenter" && \
        echo -e "\n\n# enable agent ssl\n[agents]\nuse_ssl = True" | tee -a /etc/opscenter/opscenterd.conf
}

# =========================================
# 
# Main
#
echo "[INFO] Modify the aptitude repository source list file (/etc/apt/sources.list.d/datastax.sources.list)" && \
    echo "deb https://debian.datastax.com/enterprise stable main" | \
        tee -a /etc/apt/sources.list.d/datastax.sources.list

echo "[INFO] Add the DataStax repository key to your aptitude trusted keys" && \
    curl -L https://debian.datastax.com/debian/repo_key | apt-key add -

echo "[INFO] Install the OpsCenter package using the APT Package Manager" && \
    apt-get update && \
        apt-get install -y opscenter=${DATASTAX_OPSCENTER_VERSION}

echo "[INFO] Configure OpsCenter" && \
    configure_opscenter
