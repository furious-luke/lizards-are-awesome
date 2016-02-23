FROM alpine:edge

RUN mkdir -p /usr/local/bin /usr/local/app /usr/local/plink
WORKDIR /usr/local

ADD repositories /etc/apk/repositories

RUN apk add --update \
    python \
    py-pip \
    cython \
    cython-dev \
    py-numpy@testing \
    py-numpy-dev@testing \
    py-scipy@testing \
    gsl

RUN apk add --update --virtual build-dependencies \
    python-dev \
    build-base \
    curl \
    gsl-dev \
    && pip install pandas xlrd \
    && curl -s -k -L https://github.com/rajanil/fastStructure/archive/master.tar.gz | tar xz \
    && mv fastStructure-master fastStructure \
    && cd fastStructure/vars \
    && python setup.py build_ext --inplace \
    && cd .. \
    && python setup.py build_ext --inplace \
    && apk del --force build-dependencies

RUN apk del py-numpy-dev cython-dev && rm -rf /var/cache/apk/*

ADD convert.py /usr/local/bin
ADD plink.tgz /usr/local

WORKDIR /usr/local/app
