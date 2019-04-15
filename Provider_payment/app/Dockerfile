FROM python:3.8.0a3-alpine3.9
COPY . /
RUN chmod +x app.py
RUN pip3 install --upgrade pip && pip3 install flask
RUN pip3 install pymysql
#RUN pip3 install cryptography

EXPOSE 8000
ENTRYPOINT ["python3","app.py"]
