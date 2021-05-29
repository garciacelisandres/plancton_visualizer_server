FROM python:3.8
COPY . /code
WORKDIR /code
RUN apt update && apt install -y --no-install-recommends \
    git \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools
RUN python3 -m venv myenv
RUN . myenv/bin/activate
RUN pip3 -q install pip --upgrade
RUN pip3 install -r /code/requirements.txt
RUN pip3 install gunicorn
CMD ["gunicorn -w 2 -b 127.0.0.1 wsgi:app"]