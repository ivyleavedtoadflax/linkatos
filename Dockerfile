FROM python:3.5-slim

ENV LANG en_US.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update -qq \
 && apt-get install -qqy \
       gcc \
 && apt-get autoclean \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
 && pip install --upgrade pip

COPY requirements.txt /usr/local/linkatos/requirements.txt

WORKDIR /usr/local/linkatos

RUN pip install -r requirements.txt

COPY linkatos.py /usr/local/linkatos/
COPY linkatos /usr/local/linkatos/linkatos
COPY tests /usr/local/linkatos/tests
COPY test_runner.sh /usr/local/linkatos/test_runner.sh

CMD ["./linkatos.py"]
