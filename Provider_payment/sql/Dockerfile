FROM mysql
# Add a database
ENV MYSQL_DATABASE billdb
WORKDIR /hostn/
# Add the content of the sql-scripts/ directory to your image
# All scripts in docker-entrypoint-initdb.d/ are automatically
# executed during container startup
#COPY ./sql-scripts/ /docker-entrypoint-initdb.d/
COPY ./billingdb.sql/ ../docker-entrypoint-initdb.d/