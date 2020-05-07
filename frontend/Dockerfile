FROM node:alpine
  
WORKDIR /webapp

COPY package*.json ./
ENV NODE_ENV development
COPY . /webapp

RUN \
  apk update                     && \
  apk add bash                   && \
  npm install -G yarn typescript && \
  yarn

EXPOSE "8080:8080"

