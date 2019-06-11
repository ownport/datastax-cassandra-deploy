FROM ubuntu:16.04

COPY assets/ /tmp/assets

RUN /tmp/assets/sbin/install.sh

ENTRYPOINT [ "/usr/share/opscenter/bin/opscenter", "-f" ]