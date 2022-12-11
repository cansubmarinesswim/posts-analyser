FROM python:3.8-slim-buster
WORKDIR /gateway
COPY gateway .
COPY db_controller/proto /db_controller/proto
LABEL maintainer="<tkurkowski@student.agh.edu.pl>"

RUN { \
    pip install --upgrade pip ; \
    pip install . ; \
}
