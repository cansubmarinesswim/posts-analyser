import gettext

from grpc import StatusCode

from google.protobuf import any_pb2
from google.rpc import code_pb2
from google.rpc import error_details_pb2
from google.rpc import status_pb2
import grpc
from grpc_status import rpc_status

from db_controller.proto import db_controller_pb2_grpc, db_controller_pb2

from db_controller.logger import Logger
from db_controller.db_connection import DbConnection
from db_controller.user_policy import UserPolicy

from db_controller.exceptions import (
    DbConnectionError,
    ManageUserError,
)


class DbControllerService(db_controller_pb2_grpc.PostsAnalyserDbControllerServicer):
    def __init__(self, args):
        self._db_connection = DbConnection(args.db_user, args.db_pass, args.db_name)
        self._user_policy = UserPolicy(
            args.passwd_min_length,
            args.passwd_max_length,
            args.passwd_uppercase,
            args.passwd_numbers,
            args.passwd_special,
        )
        self.logger = Logger(
            name="posts_analyser_db_controller",
            console_log_level=args.console_log_level,
            file_log_level=args.file_log_level,
            file_log_dir=args.file_log_dir,
        ).logger
        self.logger.info("gRPC posts_analyser_db_controller started.")

    def _create_rich_error_status(self, message, grpc_error):
        return status_pb2.Status(
            code=code_pb2.__getattribute__(grpc_error.name),
            message=message,
            details=None,
        )

    def AddUserEntry(self, request, context):
        username = request.username
        password = request.password
        try:
            self._user_policy.validate_user_policy(username, password)
            self._db_connection.add_user(username, password)

        except (DbConnectionError, ManageUserError) as e:
            self.logger.warning(e.message)
            rich_status = self._create_rich_error_status(
                e.message,
                e.grpc_error,
            )
            context.abort_with_status(rpc_status.to_status(rich_status))

        except Exception as e:
            self.logger.error(e)
            rich_status = self._create_rich_error_status(
                "Unknown Error",
                StatusCode.UNKNOWN,
            )
            context.abort_with_status(rpc_status.to_status(rich_status))

        return db_controller_pb2.AddUserEntryResponse()

    def RemoveUserEntry(self, request, context):
        username = request.username
        try:
            self._db_connection.remove_user(username)

        except (DbConnectionError, ManageUserError) as e:
            self.logger.warning(e.message)
            rich_status = self._create_rich_error_status(
                e.message,
                e.grpc_error,
            )
            context.abort_with_status(rpc_status.to_status(rich_status))

        except Exception as e:
            self.logger.error(e)
            rich_status = self._create_rich_error_status(
                "Unknown Error",
                StatusCode.UNKNOWN,
            )
            context.abort_with_status(rpc_status.to_status(rich_status))

        return db_controller_pb2.RemoveUserEntryResponse()

    def VerifyUserCredentials(self, request, context):
        username = request.username
        password = request.password

        try:
            self._db_connection.validate_user_credentals(username, password)
            self.logger.info(f"Credentials valid for {username}.")
            return db_controller_pb2.VerifyUserCredentialsResponse()

        except DbConnectionError as e:
            self.logger.warning(e.message)
            rich_status = self._create_rich_error_status(
                e.message,
                e.grpc_error,
            )
            context.abort_with_status(rpc_status.to_status(rich_status))
        except Exception as e:
            self.logger.error(e)
            rich_status = self._create_rich_error_status(
                "Unknown Error",
                StatusCode.UNKNOWN,
            )
            context.abort_with_status(rpc_status.to_status(rich_status))

        return db_controller_pb2.VerifyUserCredentialsResponse()

    def AddPostEntry(self, request, context):
        author = request.author
        title = request.title
        content = request.content

        try:
            self._db_connection.create_post(author, title, content)
            self.logger.info(
                f'Post "{title}" created successfully by "{author}"'
            )
            self.logger.debug(f"Post content:\n{content}")

        except DbConnectionError as e:
            self.logger.warning(e.message)
            rich_status = self._create_rich_error_status(
                e.message,
                e.grpc_error,
            )
            context.abort_with_status(rpc_status.to_status(rich_status))
        except Exception as e:
            self.logger.error(e)
            rich_status = self._create_rich_error_status(
                "Unknown Error",
                StatusCode.UNKNOWN,
            )
            context.abort_with_status(rpc_status.to_status(rich_status))
        return db_controller_pb2.AddPostEntryResponse()

    def ModifyPostEntry(self, request, context):
        id = request.id
        title = request.title
        content = request.content
        classification = request.classification

        try:
            self._db_connection.modify_post(
                id, title, content, classification
            )
            self.logger.info(
                f'Post with "{id}" modified successfully."'
            )

        except DbConnectionError as e:
            self.logger.warning(e.message)
            rich_status = self._create_rich_error_status(
                e.message,
                e.grpc_error,
            )
            context.abort_with_status(rpc_status.to_status(rich_status))
        except Exception as e:
            self.logger.error(e)
            rich_status = self._create_rich_error_status(
                "Unknown Error",
                StatusCode.UNKNOWN,
            )
            context.abort_with_status(rpc_status.to_status(rich_status))
        return db_controller_pb2.ModifyPostEntryResponse()

    def GetPostEntry(self, request, context):
        id = request.id

        try:
            post = self._db_connection.get_post(id)
            self.logger.info(f'Post with id "{id}" loaded successfully."')
            return db_controller_pb2.GetPostEntryResponse(
                post_entry=self._parse_post_entry_as_message(post)
            )

        except DbConnectionError as e:
            self.logger.warning(e.message)
            rich_status = self._create_rich_error_status(
                e.message,
                e.grpc_error,
            )
            context.abort_with_status(rpc_status.to_status(rich_status))

        except Exception as e:
            self.logger.error(e)
            rich_status = self._create_rich_error_status(
                "Unknown Error",
                StatusCode.UNKNOWN,
            )
            context.abort_with_status(rpc_status.to_status(rich_status))

        return db_controller_pb2.GetPostEntryResponse()

    def GetPostsEntries(self, request, context):
        try:
            posts = self._db_connection.get_posts()
            posts_message = [
                self._parse_post_entry_as_message(post) for post in posts
            ]
            self.logger.debug(f"{len(posts_message)} posts loaded successfully.")
            return db_controller_pb2.GetPostsEntriesResponse(
                post_entries=posts_message
            )

        # possibly, remove DbConnectionError handling, since now it does not occur
        except DbConnectionError as e:
            self.logger.warning(e.message)
            rich_status = self._create_rich_error_status(
                e.message,
                e.grpc_error,
            )
            context.abort_with_status(rpc_status.to_status(rich_status))
        except Exception as e:
            self.logger.error(e)
            rich_status = self._create_rich_error_status(
                "Unknown Error",
                StatusCode.UNKNOWN,
            )
            context.abort_with_status(rpc_status.to_status(rich_status))

        return db_controller_pb2.GetPostsEntriesResponse()

    def _parse_post_entry_as_message(self, post_db_entry):
        return (
            db_controller_pb2.PostEntry(
                id=post_db_entry.id,
                title=post_db_entry.author,
                created_at=post_db_entry.created_at.replace(
                    microsecond=0
                ).isoformat(),
                modified_at=post_db_entry.modified_at.replace(
                    microsecond=0
                ).isoformat()
                if post_db_entry.modified_at is not None
                else None,
                tagged_at=post_db_entry.tagged_at.replace(
                    microsecond=0
                ).isoformat()
                if post_db_entry.tagged_at is not None
                else None,
                classification=post_db_entry.classification,
            )
            if post_db_entry is not None
            else None
        )