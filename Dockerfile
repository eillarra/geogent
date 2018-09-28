FROM python:3.7-alpine

WORKDIR /app
COPY requirements.txt /app/

# ensure Alpine Linux includes the necessary packages
RUN apk add --no-cache \
        libxml2 libxslt \
    && apk add --virtual .build build-base \
        libxml2-dev libxslt-dev \
    && pip install --no-cache-dir -q -r requirements.txt \
    && apk del .build

COPY . /app

CMD gunicorn geogent:app
