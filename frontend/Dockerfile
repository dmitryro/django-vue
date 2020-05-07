FROM node:alpine
WORKDIR /webapp
COPY package*.json ./
ENV NODE_ENV development
COPY . /webapp
RUN \
  echo 'export PATH="$(yarn global bin):$PATH"' >>  ~/.bashrc && \
  apk update                     && \
  apk add bash                   && \
  apk add python3                && \
  npm install -G yarn typescript && \
  npm install -G @quasar/cli && \
  yarn
EXPOSE "8080:8080"

