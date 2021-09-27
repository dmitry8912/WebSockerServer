## Simple non-blocking websocket server with jRPC requests

### Environment variables:

WSS_PORT - specifies listening port

WSS_HOST - specifies host, *unnecessary param*

### jRPC methods

#### send_echo
sends response to requested client

requires one parameter - message

#### send_message
sends message to connected clients

requires two parameters:
id (leave '*' for all clients), and message


### Docker reference
To build an image just run:

docker build -t <your_image_name> .

To run:

docker exec --rm -it -p 8765:8765 <your_image_name>

Optionally, you can pass an env variables to set host and port

docker exec --rm -it --env WSS_HOST=localhost --env WSS_PORT=8765 -p 8765:8765 <your_image_name>

Note, that you may set only WSS_PORT, and don`t forget to pass your port outside