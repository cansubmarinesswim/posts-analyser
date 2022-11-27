import grpc

from db_controller.proto import db_controller_pb2, db_controller_pb2_grpc


def run():
    channel = grpc.insecure_channel("0.0.0.0:60052")
    stub = db_controller_pb2_grpc.PostsAnalyserDbControllerStub(channel)

    username = "user"
    password = "Pass123!"

    ## TEST ADDUSER
    try:
        response = stub.AddUserEntry(
            db_controller_pb2.AddUserEntryRequest(username=username, password=password)
        )
    except grpc.RpcError as e:
        print(e.code())
        print(e.details())
        return
    else:
        print(f"AddUser OK")

    # AddPostEntry
    try:
        response = stub.AddPostEntry(
            db_controller_pb2.AddPostEntryRequest(
                title="tytul",
                author=username,
                content="some_text",
            )
        )
    except grpc.RpcError as e:
        print(e.code())
        print(e.details())
        return
    else:
        print(f"AddPostEntry OK")

    ## GetPostEntry
    try:
        response = stub.GetPostEntry(
            db_controller_pb2.GetPostEntryRequest(
                id=1,
            )
        )
    except grpc.RpcError as e:
        print(e.code())
        print(e.details())
        return
    else:
        print(f"GetPostEntry OK")

    ## AddPostEntry
    try:
        response = stub.ModifyPostEntry(
            db_controller_pb2.ModifyPostEntryRequest(
                id=1,
                title="tytul2",
                content="some text 2",
                classification='{"ok":1}',
            )
        )
    except grpc.RpcError as e:
        print(e.code())
        print(e.details())
        return
    else:
        print(f"ModifyPostEntry OK")

    ## GetPostEntry
    try:
        response = stub.GetPostEntry(
            db_controller_pb2.GetPostEntryRequest(
                id=1,
            )
        )
    except grpc.RpcError as e:
        print(e.code())
        print(e.details())
        return
    else:
        print(f"GetPostEntry OK")


if __name__ == "__main__":
    run()
