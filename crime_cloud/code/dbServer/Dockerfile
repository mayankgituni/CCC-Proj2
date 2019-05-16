FROM python:3.7.3-stretch

###################################################################
# File Name	    : Dockerfile
# Description	: This script is used to build docker image for the
#                   dbServer.
# Args         	: N/A
# Author       	: mtomar
###################################################################

MAINTAINER Web-db

COPY ./app/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app /app

EXPOSE 50000 50001

CMD [ "bash", "setup.sh"]