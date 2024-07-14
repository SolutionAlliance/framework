FROM python:3.6-alpine

ENV FLASK_APP manager.py
ENV FLASK_CONFIG production
ENV PYTHONOPTIMIZE 1
ENV LANG C.UTF-8
RUN echo 'Asia/Shanghai' > /etc/timezone
ENV TZ='Asia/Shanghai'

RUN adduser -D manager
USER manager

WORKDIR /home/manager

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/prod.txt

COPY app app
COPY migrations migrations
COPY manager.py config.py boot.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
