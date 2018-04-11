FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y python3-pip curl

EXPOSE 80 80
RUN mkdir /opt/filerestapi /opt/filerestapi/db /opt/filerestapi/filestorage

COPY . /opt/filerestapi

RUN python3 -m pip install -r /opt/filerestapi/etc/requirements.txt
RUN chmod +x /opt/filerestapi/bin/run.sh /opt/filerestapi/tests/run.sh
RUN python3 /opt/filerestapi/bin/manager.py \
        --dbpath '/opt/filerestapi/db/sql.db' \
        --filestorage_path /opt/filerestapi/filestorage/

CMD /opt/filerestapi/bin/run.sh
