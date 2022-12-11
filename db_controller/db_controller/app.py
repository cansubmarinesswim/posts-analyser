from argparse import ArgumentParser
from concurrent import futures
from signal import signal, SIGTERM, SIGINT
from os import getenv
from pathlib import Path

import grpc

from db_controller.proto import db_controller_pb2_grpc
from db_controller.db_controller_service import DbControllerService
from db_controller.logger import Logger


def parser():
    parser = ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "--db-user",
        dest="db_user",
        default=getenv("APP_DB_USER"),
        help="The username that service will use while communicating with database.",
        type=str,
    )
    parser.add_argument(
        "--db-pass",
        dest="db_pass",
        default=getenv("APP_DB_PASS"),
        help="A password for username specified in --db-user.",
        type=str,
    )
    parser.add_argument(
        "--db-name",
        dest="db_name",
        default=getenv("APP_DB_NAME"),
        help="A database name for service to connect to.",
        type=str,
    )
    parser.add_argument(
        "--passwd-min-length",
        dest="passwd_min_length",
        default=getenv("PASSWD_MIN_LENGTH", 8),
        help="The minimum number of characters required in a user's password.",
        type=int,
    )
    parser.add_argument(
        "--passwd-max-length",
        dest="passwd_max_length",
        default=getenv("PASSWD_MAX_LENGTH", 128),
        help="The maximum number of characters allowed in a user's password.",
        type=int,
    )
    parser.add_argument(
        "--passwd-uppercase",
        dest="passwd_uppercase",
        default=getenv("PASSWD_UPPERCASE", 1),
        help="The minimum number of uppercase characters required in a user's password.",
        type=int,
    )
    parser.add_argument(
        "--passwd-numbers",
        dest="passwd_numbers",
        default=getenv("PASSWD_NUMBERS", 1),
        help="The minimum number of numbers required in a user's password.",
        type=int,
    )
    parser.add_argument(
        "--passwd-special",
        dest="passwd_special",
        default=getenv("PASSWD_SPECIAL", 1),
        help="The minimum number of special characters required in a user's password.",
        type=int,
    )
    parser.add_argument(
        "--console-log-level",
        dest="console_log_level",
        default=getenv("CONSOLE_LOG_LEVEL", "INFO"),
        help="Console logging level.",
        type=str,
    )
    parser.add_argument(
        "--file-log-level",
        dest="file_log_level",
        default=getenv("FILE_LOG_LEVEL", "INFO"),
        help="File logging level.",
        type=str,
    )
    parser.add_argument(
        "--file-log-dir",
        dest="file_log_dir",
        default=getenv("FILE_LOG_DIR", str(Path().absolute() / "logs")),
        help="A directory for logs storage.",
        type=str,
    )

    args = parser.parse_args()

    if args.db_user is None:
        raise parser.error(
            "--db-user option must be specified if APP_DB_USER environmental variable is not present."
        )
    if args.db_pass is None:
        raise parser.error(
            "--db-pass option must be specified if APP_DB_PASS environmental variable is not present."
        )
    if args.db_name is None:
        raise parser.error(
            "--db-name option must be specified if APP_DB_NAME environmental variable is not present."
        )

    return args


class Server:
    @staticmethod
    def run(args, port: int = 60052, max_workers: int = 10):

        logger = Logger(
            name="__name__",
            console_log_level=args.console_log_level,
            file_log_level=args.file_log_level,
            file_log_dir=args.file_log_dir,
        ).logger
        logger.info(f"Starting db controller service on port {port}...")
        try:
            pass
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
            db_controller_pb2_grpc.add_PostsAnalyserDbControllerServicer_to_server(
                DbControllerService(args), server
            )

        except Exception as e:
            logger.error(e)
            raise e

        server.add_insecure_port(f"[::]:{port}")
        server.start()

        def handle_sig(*_):
            logger.info("Shutting down gracefully.")
            done_event = server.stop(30)
            done_event.wait(30)
            logger.info("Done.")

        signal(SIGTERM, handle_sig)
        signal(SIGINT, handle_sig)

        server.wait_for_termination()


def main():
    args = parser()
    Server.run(args)


if __name__ == "__main__":
    main()
