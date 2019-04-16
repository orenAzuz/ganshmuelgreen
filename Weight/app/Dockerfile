FROM python:3.8.0a3-alpine3.9
COPY . /app
WORKDIR /app
RUN chmod +x app.py
#RUN pip3 install --upgrade pip && pip3 install flask
RUN pip3 install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["python3","app.py"]
