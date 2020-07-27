#Grab the latest alpine image
FROM python:3.8.3-alpine3.12

# Install python and pip
# RUN apk add --no-cache --update python3 py-pip bash
ADD ./requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -q -r /tmp/requirements.txt
RUN mkdir -p /var/www/kwarapp

# Add local files to the image.
# ADD ./server /var/www/igames/

# Add kwarwp files to the image.
ADD . /var/www/kwarapp

WORKDIR /var/www/kwarapp/kwarwp

# Expose is NOT supported by Heroku
EXPOSE $PORT

# Run the image as a non-root user
RUN adduser -D myuser
USER myuser

# ARG port=80

# ENV PORT=$port
# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
# CMD gunicorn --bind 0.0.0.0:$PORT wsgi
# CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "bottle_app:application"]
CMD gunicorn --bind 0.0.0.0:$PORT bottle_app
# Set-up app folder.

