FROM python:3.8.0a3-alpine3.9
COPY . /
RUN chmod +x app.py
RUN pip3 install --upgrade pip && pip3 install flask
RUN pip3 install pymysql
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev
RUN pip3 install cryptography
RUN pip3 install requests

EXPOSE 8080
ENTRYPOINT ["python3","app.py"]
