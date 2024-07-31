FROM python:3.9.19-slim
LABEL version="1.0" description="Simple FastServer for hometask"
ENV WORK_DIR=/app
WORKDIR $WORK_DIR
ADD . .
RUN rm -f .env
RUN rm Dockerfile
RUN rm -r .git
ENV SERVER_IP "0.0.0.0"
ENV SERVER_PORT 8000
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "-m", "API_up" ]