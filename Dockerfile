FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY whrbcatalog/ .

ENV FLASK_APP application.py

CMD [ "flask", "run", "--host=0.0.0.0" ]
