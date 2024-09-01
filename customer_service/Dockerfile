# syntax=docker/dockerfile:1
FROM python:3.12-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Install dependencies for building librdkafka and Python packages
RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    openssl-dev \
    cyrus-sasl-dev \
    zlib-dev \
    curl \
    make \
    bash

# Install librdkafka from source
RUN curl -L https://github.com/confluentinc/librdkafka/archive/refs/tags/v2.5.0.tar.gz | tar xz && \
    cd librdkafka-2.5.0 && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf librdkafka-2.5.0



WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/