# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
RUN apt-get -y install git


COPY req.txt req.txt
RUN pip3 install -r req.txt
RUN pip3 install protobuf==3.20.0

COPY . /python-docker
EXPOSE 5000
ENTRYPOINT [ "python3" ]
CMD [ "index.py"]