FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY whrbcatalog whrbcatalog

ENV FLASK_APP whrbcatalog.application.py

CMD [ "flask", "run", "--host=0.0.0.0" ]
