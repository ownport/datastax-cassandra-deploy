FROM alpine:3.9

RUN apk add --update \
        bash \
        curl \
        jq \
        python3 && \
    pip3 install --upgrade pip && \
    pip3 install \
        pytest \
        pytest-cov \
        pytest-mock \
        pytest-xdist \
        pytest-benchmark \
        PyYAML==5.1.1 \
        requests==2.22.0

