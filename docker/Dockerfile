FROM alpine:edge

RUN mkdir -p /usr/local/bin /usr/local/app /usr/local/plink
WORKDIR /usr/local

ADD repositories /etc/apk/repositories

RUN apk add --update \
    python \
    cython \
    openblas@community \
    py-numpy@community \
    py-scipy@testing \
    gsl \
    && rm -rf /var/lib/apt/lists/*

RUN apk add --update \
    python-dev \
    build-base \
    curl \
    gsl-dev \
    cython-dev \
    py-numpy-dev@community \
    openblas-dev@community \
    py2-pip \
    && pip install pandas xlrd python-slugify \
    && curl -s -k -L https://github.com/rajanil/fastStructure/archive/master.tar.gz | tar xz \
    && mv fastStructure-master fastStructure \
    && cd fastStructure/vars \
    && python setup.py build_ext --inplace \
    && cd .. \
    && python setup.py build_ext --inplace \
    && apk del --force python-dev build-base curl gsl-dev cython-dev py-numpy-dev py-pip \
    && rm -rf /var/lib/apt/lists/*

ADD convert.py /usr/local/bin
ADD plink.tgz /usr/local

WORKDIR /usr/local/app
