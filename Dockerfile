FROM library/python:3.7-slim

COPY requirements.txt /app/
COPY main.py /app/
COPY setup.py /app/

WORKDIR /app

RUN pip3.7 install -r requirements.txt
RUN pip3.7 install .

EXPOSE 8080

CMD aio-demo-serve
