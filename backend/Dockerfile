# start from an official image
FROM python:3.8.1

# arbitrary location choice: you can change the directory
RUN mkdir -p /opt/services/backend
WORKDIR /opt/services/backend

# install our dependencies
# we use --system flag because we don't need an extra virtualenv
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN pip install -r requirements.txt

# copy our project code
COPY . /opt/services/backend
RUN python manage.py collectstatic 
RUN ln -s /opt/services/backend/static /static
RUN chmod +x /entrypoint.sh
EXPOSE 8000
