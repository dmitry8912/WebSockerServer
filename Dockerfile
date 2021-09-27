FROM alpine:latest
RUN apk add python3 py-pip
RUN mkdir /app
ADD ./src/main.py /app
ADD ./requirements.txt /app
ADD ./run.sh /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod +x /app/run.sh
EXPOSE 8765
ENTRYPOINT ["/app/run.sh"]