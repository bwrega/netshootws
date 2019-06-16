FROM nicolaka/netshoot

RUN pip install web.py requests

ADD diagnostic_server.py /diagnostic_server.py

EXPOSE 8080
ENTRYPOINT [ "/diagnostic_server.py" ]

