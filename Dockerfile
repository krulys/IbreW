FROM python

COPY ./source ./source
COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

ENV DB_USER="root"
ENV DB_HOST="172.17.0.2"
ENV DB_PASS="GYiPyR18LZ"

EXPOSE 80

ENTRYPOINT [ "python", "-m","source.server.server" ]