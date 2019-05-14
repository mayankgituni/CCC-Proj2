FROM python:3-alpine

MAINTAINER Web-Compose

# RUN apk add --no-cache python3 && \
#     python3 -m ensurepip && \
#     rm -r /usr/lib/python*/ensurepip && \
#     pip3 install --upgrade pip setuptools && \
#     if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
#     if [[ ! -e /usr/bi n/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
#     rm -r /root/.cache

RUN apk add --update \
    curl \
    gcc \
    git \
    libc-dev \
    nodejs \
    npm \
    rm -rf /var/cache/apk/*

COPY ./app/requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

COPY ./app/frontend/package.json /app/frontend/package.json
WORKDIR /app/frontend

RUN npm install create-react-app
RUN npm install 
RUN npm run build

COPY ./app /app
EXPOSE 50000 50001
WORKDIR /app/backend

CMD [ "python3", "server.py"]