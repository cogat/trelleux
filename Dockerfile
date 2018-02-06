# The Dockerfile defines an application’s image content via one or more build commands that configure that image.
# Once built, you can run the image in a container.

FROM python:3

# Copy in your requirements file. If you install this way, it uses the docker
# cache, whereas if you install it from /app, it reinstalls every time the
# app has changed.
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=0

# set up entrypoint
COPY /scripts/entrypoint.sh /entrypoint.sh
ENTRYPOINT /entrypoint.sh

# wait-for-it is a script that pauses until a service comes up
COPY /scripts/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copy your application app to the container, ignoring .dockerignore files.
RUN mkdir /app/
WORKDIR /app/
COPY . /app/
