FROM python:3.8
WORKDIR /code

RUN apt update && apt install -y --no-install-recommends
RUN pip3 -q install pip --upgrade

COPY . .
RUN pip install -r /code/requirements.txt
RUN pip install pymongo[srv]
RUN pip install gunicorn

# SSL certificates
ARG CERTFILE
ARG KEYFILE
COPY CERTFILE ./certfile.pem
COPY KEYFILE ./keyfile.pem

CMD gunicorn -w 2 -b 0.0.0.0:51000 --pythonpath /code --certfile=certfile.pem --keyfile=keyfile.pem wsgi:app