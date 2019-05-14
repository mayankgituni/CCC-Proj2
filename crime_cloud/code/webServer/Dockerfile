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

# COPY ./app/frontend/yarn.lock /app/yarn.lock

# WORKDIR /app
# RUN yarn upgrade --latest

# COPY ./app/requirements.txt /app/requirements.txt


# RUN pip3 install --upgrade pip setuptools
# RUN pip3 install -r requirements.txt

# COPY ./app/frontend/package.json /app/frontend/package.json
# WORKDIR /app/frontend

# RUN npm install create-react-app
# RUN npm install
# RUN npm run build

# COPY ./app /app
# EXPOSE 50000 50001
# WORKDIR /app/backend

# CMD [ "python3", "server.py"]