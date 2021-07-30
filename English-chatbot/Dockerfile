FROM rasa/rasa:2.7.0-full

WORKDIR /app

COPY ./*.yml /app/
COPY ./data /app/data/
COPY ./tests /app/tests/
COPY ./models/ app/models/

VOLUME /app
VOLUME /app/data
VOLUME /app/models

WORKDIR /app
CMD ["run","-m","/app/models","--credentials","/app/credentials.yml","--enable-api","--cors","*","--debug"]
