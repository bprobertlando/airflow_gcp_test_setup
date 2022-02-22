FROM python:3.8-slim-buster

WORKDIR /usr/src/app

USER root

RUN apt-get update -y && apt-get install -y python3-pip git

COPY scripts/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY scripts/* ./ 

ARG GITHUB_SHA
ENV GITHUB_SHA=$GITHUB_SHA

ENTRYPOINT [ "python", "./entrypoint.py" ]
