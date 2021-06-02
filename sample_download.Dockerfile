FROM pytorch/pytorch:1.7.1-cuda11.0-cudnn8-runtime
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
COPY database /code/database
COPY production /code/production
COPY quantificationlib /code/quantificationlib
COPY results /code/results
COPY sample_download /code/sample_download
COPY model.pt /code/model.pt
COPY .env /code/.env
RUN pip install -r /code/quantificationlib/requirements.txt
RUN pip install -r /code/sample_download/requirements.txt
RUN pip install pymongo[srv]