FROM python:3.7.3-stretch

MAINTAINER Web-db

COPY ./app/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app /app

EXPOSE 50000 50001

CMD ["python3", "generate_geofile.py"]
# CMD [ "bash", "setup.sh" ]