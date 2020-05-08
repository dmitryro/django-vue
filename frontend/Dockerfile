FROM mhart/alpine-node:12
  
WORKDIR /webapp

COPY package*.json ./

RUN apk add --no-cache make gcc g++ python

ENV NODE_ENV development
COPY . /webapp

RUN \
  apk update                     && \
  apk add bash                   && \
  npm install -G yarn            && \
  yarn

EXPOSE "8080:8080"


