FROM library/python:3.7-slim

COPY requirements.txt /app/
COPY dist/aio_demo-*.whl /app/

WORKDIR /app

RUN pip3.7 install -r requirements.txt
RUN pip3.7 install aio_demo-*.whl

EXPOSE 8080

CMD ["aio-demo-serve"]
