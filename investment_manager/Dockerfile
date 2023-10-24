FROM python:3.10

ENV PYTHONUNBUFFERED 1 


RUN pip install --upgrade pip

COPY requirements.txt . 

RUN pip install -r requirements.txt

RUN mkdir /app

COPY . /app
WORKDIR /app


COPY ./entrypoint.sh /

ENTRYPOINT ["sh", "/entrypoint.sh"]