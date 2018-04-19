FROM python:3.6-alpine3.7

# ensure Alpine Linux includes the packages necessary for `lxml`
RUN apk add --update --no-cache build-base git \
    py3-lxml py3-libxml2 libxml2-dev libxslt-dev

# install Pipenv
RUN pip install --upgrade pip && pip install pipenv

# install app
RUN mkdir /app
WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --deploy --system
COPY . /app

CMD gunicorn geogent:app
