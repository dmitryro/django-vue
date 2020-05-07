FROM node:alpine
WORKDIR /webappadmin
COPY package*.json ./
ENV NODE_ENV development
COPY . /webappadmin

RUN \
  apk update                     && \
  apk add bash                   && \
  apk add git                    && \
  apk add python3                && \
  npm install -G yarn typescript && \
  yarn 

EXPOSE "9527:9527"
EXPOSE "8081:8081"


