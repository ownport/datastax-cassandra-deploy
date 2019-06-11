#!/usr/bin/env bash

set -e

apt-get update 

/tmp/assets/sbin/install-tools.sh
/tmp/assets/sbin/install-java.sh
/tmp/assets/sbin/install-datanode.sh
/tmp/assets/sbin//cleanup.sh

rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/oracle-jdk8-installer

