FROM python:3.12-slim-bookworm
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /mnt/logs/

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    postgresql-client \
    git && \
    rm -rf /var/lib/apt/lists/*

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt pyuwsgi

RUN apt-get --purge autoremove -y \
    build-essential \
    python3-dev

ADD uwsgi.ini /etc/uwsgi/app.ini

ADD .circleci/wait-for-postgres.sh /circleci/
RUN chmod +x /circleci/wait-for-postgres.sh

ADD ./b3 /app

ARG SOURCE_COMMIT
ENV SENTRY_RELEASE $SOURCE_COMMIT

EXPOSE 3030 8000

CMD ["/usr/local/bin/uwsgi", "--ini", "/etc/uwsgi/app.ini"]
