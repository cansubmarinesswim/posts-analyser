FROM python:3.8-slim-buster
WORKDIR /db-controller
COPY . .
LABEL maintainer="<tkurkowski@student.agh.edu.pl>"

RUN { \
    pip install --upgrade pip ; \
    pip install . ; \
}
