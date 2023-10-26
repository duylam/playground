# Setup

> Extracted from https://grpc.io/docs/languages/python/basics/

- Python v3
- Install Docker

# How to use

### 1. Compile protobuf

```bash
python3 -m venv /tmp/venv; /tmp/venv/bin/pip install -r python-app/requirements.txt
cd python-app
cp -r ../protos/app/. ./grpc_out/; \
  /tmp/venv/bin/python -m grpc_tools.protoc \
    -I. -I../protos/ \
    --python_out=. --pyi_out=. --grpc_python_out=. \
    ./grpc_out/helloworld.proto; \
  /tmp/venv/bin/python -m grpc_tools.protoc \
    --include_source_info --include_imports \
    -I. -I../protos/ \
    --descriptor_set_out=../protos/out/descriptor-set.pb \
    ./grpc_out/helloworld.proto ../protos/google/rpc/error_details.proto
```

What to have:
- The compiled Python code at `./python-app/grpc-out/`
- The compiled [descriptor](https://protobuf.com/docs/descriptors) file `./protos/out/descriptor-set.pb`

### 2. Run the gRPC Python server

```bash
cd python-app; PORT=3020 /tmp/venv/bin/python greeter_server.py
```

What to have:
- A gRPC server listening on port 3020 with Reflection service available. You can use Postman to test it out

### 3. Start proxy with JSON Transoder

Run the below command

```bash
docker compose -f json-transcoder/docker-compose.yaml up
```

What to have:
- An HTTP server at `http://localhost:3000/sayHello` which proxies gRPC server at `localhost:3020`
- Envoy runs with `debug` log level
- Terminate the command and run again for applying config changes

To test the transcoder, run

```bash
curl --http1.1 -v -N 'http://localhost:3000/helloworld.Greater/sayHelloStreamReply' \
    --header 'Content-Type: application/json' \
    --header 'x-my-header: my-value' \
    --data '{
        "name": "hello"
    }'
```

