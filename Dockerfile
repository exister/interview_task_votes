FROM python:3.5
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD entrypoint.sh /app/
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["runserver"]

ADD . /app/
