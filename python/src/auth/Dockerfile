FROM python:3.12.3-slim-bullseye

RUN apt-get update \ 
  && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential default-libmysqlclient-dev pkg-config \
  && pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY requirement.txt .

RUN pip install --no-cache-dir --requirement requirement.txt

COPY . .

EXPOSE 8080

CMD [ "python3", "server.py" ]