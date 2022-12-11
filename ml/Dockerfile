FROM python:3.8-slim

WORKDIR /opt/posts_sentiment_analyser

COPY requirements.txt .
RUN { \
    python -m pip install --upgrade pip setuptools wheel ;\
    pip install torch --extra-index-url https://download.pytorch.org/whl/cpu ;\
    pip install -r requirements.txt ;\
}

COPY . .
RUN pip install .

ENTRYPOINT [ "waitress-serve", "--call", "posts_sentiment_analyser:create_app" ]