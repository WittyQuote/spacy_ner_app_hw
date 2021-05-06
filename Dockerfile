FROM python:3.6-slim-buster

COPY app .
RUN apt-get -y update && apt-get install -y sqlite3 libsqlite3-dev
RUN python -m pip install -r requirements.txt
RUN python -m spacy download "en_core_web_sm"

ENTRYPOINT python spacy_fun_app.py