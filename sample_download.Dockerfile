FROM pytorch/pytorch:1.7.0-cuda11.0-cudnn8-runtime
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers
COPY ../database /code/database
COPY ../production /code/production
COPY ../quantificationlib /code/quantificationlib
COPY ../results /code/results
COPY ../sample_download /code/sample_download
COPY ../model.pt /code/model.pt
RUN pip install -r /code/sample_download/requirements.txt