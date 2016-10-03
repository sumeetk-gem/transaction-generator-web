# Dockerfile for Cyclos project (http://www.cyclos.org)
FROM python:2.7

RUN pip install pika flask

ENV SAMPLE_APP_HOME /root/sampleapp
ADD . ${SAMPLE_APP_HOME}
WORKDIR ${SAMPLE_APP_HOME}

RUN  chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
