FROM python:3.12.0-slim-bullseye

# Install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    gcc default-libmysqlclient-dev pkg-config \
    build-essential python3-dev \
    && pip install --upgrade pip

# create a directory to work from (app)
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE 5000

CMD [ "python","server.py" ]