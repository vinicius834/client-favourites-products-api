FROM python:3.7-alpine
MAiNTAINER Vinicius Barbosa de Suza

ENV PYTHONUBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN \
 apk add --no-cache --virtual .build-deps gcc musl-dev && \
 pip install -r /requirements.txt --no-cache-dir && \
 apk --purge del .build-deps


RUN mkdir /client-favourites-products-api
WORKDIR /client-favourites-products-api
COPY ./* /client-favourites-products-api

RUN adduser -D user
USER user
