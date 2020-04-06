FROM python:3.7.2-slim

LABEL maintainer="Raja Y"

ARG APP_HOME=/usr/local/covid19dashboard

ENV PYTHONPATH=${APP_HOME}

WORKDIR ${APP_HOME}


COPY . ${APP_HOME}

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR ${APP_HOME}/app

EXPOSE 8501

CMD [ "bash", "run.sh" ]