FROM python:3.8
WORKDIR /code

RUN apt update && apt install -y --no-install-recommends
RUN python3 -m venv myenv
RUN . myenv/bin/activate
RUN pip3 -q install pip --upgrade

COPY . .
RUN pip3 install -r /code/requirements.txt
RUN apt-get -y install gunicorn3
RUN gunicorn --help
CMD ["gunicorn -w 2 -b 127.0.0.1:51000 wsgi:app"]