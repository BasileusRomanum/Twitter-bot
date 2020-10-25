FROM python:3.9-alpine

COPY bots/config.py /bots/
COPY bots/Korwinizmy.py /bots/
COPY bots/cytaty.txt /bots
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bots
CMD ["python3", "Korwinizmy.py"]
