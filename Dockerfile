FROM nickgryg/alpine-pandas
MAINTAINER OLEKSANDR LAVRUSENKO

ENV PYTHONUNBUFFERED 1
COPY ./docker_req.txt ./docker_req.txt
RUN apk add  --no-cache postgresql-client
RUN apk add  --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev gcc musl-dev libffi-dev openssl-dev python3-dev
RUN pip install -r /docker_req.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN adduser -D user
USER user