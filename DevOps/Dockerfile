#FROM python:3.6-slim
#FROM python:3.7-alpine
FROM tiangolo/uwsgi-nginx:python3.6-alpine3.7
#FROM python:3.8.0a3-alpine3.9

ENV PYTHONPATH=/app

RUN mkdir -p /app/templates
WORKDIR /app

COPY requirements.txt .
#RUN pip3 install -r requirements.txt --src /usr/local/src
RUN pip3 install -r requirements.txt
#RUN pip3 install flask

COPY templates/index.html templates/
COPY app.py .
COPY reload.sh .
RUN chmod +x app.py
RUN chmod +x reload.sh

EXPOSE 5000

#ENTRYPOINT [ "python3", "app.py" ]
CMD python3 app.py

#docker build -t devops .
#docker run -itd -p 8000:5000 devops
