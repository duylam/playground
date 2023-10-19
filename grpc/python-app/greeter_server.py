# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc
import os
from typing import Iterable
import time
from grpc_reflection.v1alpha import reflection
from grpc_out import helloworld_pb2, helloworld_pb2_grpc
from google.api import httpbody_pb2
from google.rpc import code_pb2, status_pb2, error_details_pb2
from google.protobuf import any_pb2
from grpc_status import rpc_status


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        logging.debug(
            "Received invocation SayHello(): %s",
            request
        )
        return helloworld_pb2.HelloReply(message="Hello, %s!" % request.name)

        # Return error following Google error standard
        #detail = any_pb2.Any()
        #detail.Pack(
        #    error_details_pb2.ErrorInfo(
        #        reason="reason1",
        #        domain="mydomain.com",
        #        metadata={
        #            "detail-message": "error message"
        #        }
        #    )
        #)
        #error_status = status_pb2.Status(
        #    code=code_pb2.INTERNAL,
        #    message="Unknown exception",
        #    details=[detail],
        #)
        #context.abort_with_status(rpc_status.to_status(error_status))


    def SayHelloStreamReply(self, request, context) -> Iterable[helloworld_pb2.HelloReply]:
        logging.debug(
            "Received invocation SayHelloStreamReply(): %s",
            request
        )
        http_payload = httpbody_pb2.HttpBody()
        http_payload.content_type = "text/plain"
        http_payload.data = bytes("done", 'ascii')
        for i in range(10):
            time.sleep(0.5)
            yield helloworld_pb2.HelloReply(message="Hello, %s!" % i, http=None)

def serve():
    port = os.getenv("PORT", 3020)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    # See https://github.com/grpc/grpc/blob/master/doc/python/server_reflection.md
    # the reflection service will be aware of "Greeter" and "ServerReflection" services.
    SERVICE_NAMES = (
        helloworld_pb2.DESCRIPTOR.services_by_name['Greeter'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(levelname)s %(message)s', level=logging.DEBUG)
    serve()
