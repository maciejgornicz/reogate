FROM python:3.12.3-alpine

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./src /app

ENTRYPOINT [ "uvicorn", "reogate.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "reogate/logging.yaml" ]
