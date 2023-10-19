# Setup

- Install Docker

# How to use

### Start proxy to HTTP

```bash
docker compose up
```

What to have:
- An HTTP server at `localhost:3000` which proxies HTTP server at `localhost:3010`
- Envoy runs with `debug` log level
- Terminate the command and run again for applying config changes

You can run the below command for a simple HTTP server on port 3010

```bash
while true; do echo -e 'HTTP/1.1 204\r\n'  | nc -l 0.0.0.0 3010; done
```

### Check help

```bash
docker run --rm envoyproxy/envoy:v1.26.6 --help
```

