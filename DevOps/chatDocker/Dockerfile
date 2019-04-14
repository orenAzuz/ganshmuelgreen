FROM python:3.6.5-alpine
# working directory
WORKDIR /app

# copy current directory into the container
ADD . /app
RUN pip3 install flask
EXPOSE 5000
RUN chmod +x entry-point.sh
ENTRYPOINT ["./entry-point.sh"] 
#ENTRYPOINT  python3 chat.py  