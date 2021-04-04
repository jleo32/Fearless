# https://docs.docker.com/language/python/build-images/

FROM python:3.8-slim-buster

# port of API
EXPOSE 3000

WORKDIR /Fearless

COPY requirements.txt requirements.txt

# install required packages
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python"]

# main file to start and run application
CMD ["main.py"]

