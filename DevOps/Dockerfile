#FROM python:3.6-slim
FROM python:3.7-alpine

#RUN mkdir -p /app/templates
#WORKDIR /app

#COPY requirements.txt .
#RUN pip3 install -r requirements.txt --src /usr/local/src
RUN pip3 install flask

RUN mkdir templates
COPY templates/index.html templates/
COPY app.py .
#RUN chmod 775 app.py

#EXPOSE 8000

#ENTRYPOINT ["python3" ]
CMD python3 app.py

#docker build -t devops .
#docker run -itd -p 8000:5000 devops