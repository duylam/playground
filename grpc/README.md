# Setup

> Extracted from https://grpc.io/docs/languages/python/basics/

- Python v3

# How to use

### Compile protobuf

```bash
python3 -m venv /tmp/venv; /tmp/venv/bin/pip install -r python-app/requirements.txt
cd python-app
cp -r ../protos/app/ ./grpc_out/; \
  /tmp/venv/bin/python -m grpc_tools.protoc \
    -I. -I../protos/ \
    --python_out=. --pyi_out=. --grpc_python_out=. \
    ./grpc_out/helloworld.proto; \
  /tmp/venv/bin/python -m grpc_tools.protoc \
    --include_source_info --include_imports \
    -I. -I../protos/ \
    --descriptor_set_out=../protos/out/descriptor-set.pb \
    ./grpc_out/helloworld.proto
```

What to have:
- The compiled Python code at `./python-app/grpc-out/`
- The compiled [descriptor](https://protobuf.com/docs/descriptors) file `./protos/out/descriptor-set.pb`

### Run the gRPC Python server

```bash
cd python-app; PORT=6000 /tmp/venv/bin/python greeter_server.py
```

What to have:
- A gRPC server listening on port 6000 with Reflection service available

