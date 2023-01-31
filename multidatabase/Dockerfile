FROM python:3.10.6
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /src
WORKDIR /src

COPY MultiDB_Django  /src/

RUN apt-get update && apt-get install -y \
    build-essential  \
    nano \
    curl
RUN apt-get install -y  gcc python3-dev


RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x /src/run_web.sh


EXPOSE 8000
CMD ["/src/run_web.sh"]
