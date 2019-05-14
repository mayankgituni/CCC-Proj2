FROM python:3-alpine

MAINTAINER Web-Compose

RUN apk add --update \
    curl \
    gcc \
    git \
    libc-dev \
    nodejs \
    npm \
    yarn \
    rm -rf /var/cache/apk/*

COPY ./app/ /app/
COPY ./app/requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install --upgrade pip setuptools
RUN pip3 install -r requirements.txt

COPY ./app/frontend/yarn.lock /app/frontend/yarn.lock
COPY ./app/frontend/package.json /app/frontend/package.json
COPY ./app/frontend/public/index.html /app/frontend/public/index.html
WORKDIR /app/frontend
RUN yarn upgrade --latest
RUN yarn install
RUN yarn build

WORKDIR /app/backend
EXPOSE 50000 50001

CMD [ "python3", "server.py"]