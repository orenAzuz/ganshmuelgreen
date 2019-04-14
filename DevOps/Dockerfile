FROM python:3.6-slim

RUN mkdir -p /app/templates
WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt --src /usr/local/src
COPY templates/index.html templates/
COPY app.py .
RUN chmod 644 app.py
EXPOSE 8000

ENTRYPOINT [ "python3" , "app.py" ]
