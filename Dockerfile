FROM python:3.8

RUN useradd -m -s /bin/bash -U appuser

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY setup.py setup.py
COPY ip_bot ip_bot
RUN pip install -e .

USER appuser

ENTRYPOINT ip-bot
