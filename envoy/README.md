# Setup

- Install Docker

# How to use

### Start proxy to HTTP

```bash
docker compose up
```

What to have:
- An HTTP server at `localhost:3000` which proxies HTTP server at `localhost:6000`
- Envoy runs with `debug` log level
- Terminate the command and run again for applying config changes

You can run the below command for a simple HTTP server on port 6000

```bash
while true; do echo -e 'HTTP/1.1 204\r\n'  | nc -l 0.0.0.0 5000; done
```

### Start proxy to gRPC

1. Compile the protobuf and the gRPC server at `./grpc/README.md` 
2. Run the below command

```bash
docker compose -f docker-compose-grpc-transcoder.yaml up
```

What to have:
- An HTTP server at `http://localhost:3000/sayHello` which proxies gRPC server at `localhost:6000`
- Envoy runs with `debug` log level
- Terminate the command and run again for applying config changes

### Check help

```bash
docker run --rm envoyproxy/envoy:v1.26.6 --help
```

