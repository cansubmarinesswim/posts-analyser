from grpc import StatusCode


class ManageUserError(Exception):
    """
    Exception for handling user management operations
    """

    def __init__(
        self,
        grpc_error=StatusCode.UNKNOWN,
        message="Managing users failed",
        web_app_message="Managing users failed",
    ):
        self.grpc_error = grpc_error
        self.message = message
        self.web_app_message = web_app_message

        super().__init__(self.message)

    def __str__(self):
        return f"gRPC error: {self.grpc_error} -> {self.message}"


class DbConnectionError(Exception):
    """
    Exception for handling database connection
    """

    def __init__(
        self,
        grpc_error=StatusCode.UNKNOWN,
        message="DbConnection failed",
        web_app_message="DbConnection failed",
    ):
        self.grpc_error = grpc_error
        self.message = message
        self.web_app_message = web_app_message

        super().__init__(self.message)

    def __str__(self):
        return f"gRPC error: {self.grpc_error} -> {self.message}"
