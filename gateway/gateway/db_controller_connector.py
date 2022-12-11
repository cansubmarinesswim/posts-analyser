import requests
import json

from google.protobuf import any_pb2
from google.rpc import code_pb2
from google.rpc import error_details_pb2
from google.rpc import status_pb2
import grpc
from grpc_status import rpc_status

from gateway.proto import db_controller_pb2, db_controller_pb2_grpc


class DbConnectorError(Exception):
    """
    Exception for handling errors from db controller service
    """

    def __init__(
        self,
        grpc_error=grpc.StatusCode.UNKNOWN,
        message="Request failed",
        web_app_message="Request failed",
    ):
        self.grpc_error = grpc_error
        self.message = message
        self.web_app_message = web_app_message
        self.status_code = 400
        super().__init__(self.message)


class DbConnector:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._channel = grpc.insecure_channel(f"{host}:{port}")
        self._stub = db_controller_pb2_grpc.PostsAnalyserDbControllerStub(self._channel)

    def _handle_rpc_error(self, rpc_error: grpc.RpcError):
        status = rpc_status.from_call(rpc_error)
        for detail in status.details:
            if detail.Is(error_details_pb2.LocalizedMessage.DESCRIPTOR):
                info = error_details_pb2.LocalizedMessage()
                detail.Unpack(info)
                raise DbConnectorError(
                    grpc_error=rpc_error.code(),
                    message=status.message,
                    web_app_message=info.message,
                )
            else:
                raise RuntimeError()

    def add_user(self, username: str, password: str):
        try:
            response = self._stub.AddUserEntry(
                db_controller_pb2.AddUserEntryRequest(
                    username=username,
                    password=password,
                )
            )
        except grpc.RpcError as rpc_error:
            self._handle_rpc_error(rpc_error)

    def remove_user(self, username: str):
        try:
            response = self._stub.RemoveUserEntry(
                db_controller_pb2.RemoveUserEntryRequest(
                    username=username,
                )
            )
        except grpc.RpcError as rpc_error:
            self._handle_rpc_error(rpc_error)

    def verify_user_credentials(self, username: str, password: str):
        try:
            response = self._stub.VerifyUserCredentials(
                db_controller_pb2.VerifyUserCredentialsRequest(
                    username=username,
                    password=password,
                )
            )
        except grpc.RpcError as rpc_error:
            self._handle_rpc_error(rpc_error)

    def add_post(self, author: str, title: str, content: str, classification):
        try:
            classification_string = json.dumps(classification)
            response = self._stub.AddPostEntry(
                db_controller_pb2.AddPostEntryRequest(
                    title=title,
                    author=author,
                    content=content,
                    classification=classification_string,
                )
            )
        except grpc.RpcError as rpc_error:
            self._handle_rpc_error(rpc_error)

    def remove_post(self, id: int):
        try:
            response = self._stub.RemovePostEntry(
                db_controller_pb2.RemovePostEntryRequest(
                    id=id,
                )
            )
        except grpc.RpcError as rpc_error:
            self._handle_rpc_error(rpc_error)

    def get_posts(self):
        try:
            response = self._stub.GetPostsEntries(
                db_controller_pb2.GetPostsEntriesRequest()
            )
            return self._parse_post_entries_to_dict(response)
        except grpc.RpcError as rpc_error:
            self._handle_rpc_error(rpc_error)

    def _parse_post_entries_to_dict(self, response):
        response_dict = {}
        for post in response.post_entries:
            response_dict[post.id] = {
                "title": post.title,
                "author": post.author,
                "content": post.content,
                "created_at": post.created_at,
                "classification": post.classification,
            }

        return response_dict
