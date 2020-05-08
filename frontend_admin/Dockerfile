FROM mhart/alpine-node:12
WORKDIR /webappadmin
COPY package*.json ./
ENV NODE_ENV development
COPY . /webappadmin

RUN \
  apk update                     && \
  apk add bash                   && \
  apk add git                    && \
  npm install -G yarn            && \
  yarn 

EXPOSE "9527:9527"
EXPOSE "8081:8081"


