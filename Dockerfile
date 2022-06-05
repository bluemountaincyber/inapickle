FROM python:latest
RUN mkdir /inapickle
COPY static /inapickle/static
COPY templates /inapickle/templates
COPY main.py /inapickle
COPY requirements.txt /inapickle
COPY database.sqlite /inapickle
RUN pip install -r /inapickle/requirements.txt
WORKDIR /inapickle
ENTRYPOINT uvicorn main:app --reload --host 0.0.0.0