import json

import bcrypt
from grpc import StatusCode
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from db_controller.models import Base, User, Post
from db_controller.exceptions import DbConnectionError


class UserAlreadyExists(DbConnectionError):
    def __init__(self, username, *, message=None):
        if not message:
            message = f'DB entry for user "{username}" is already present.'
        super().__init__(StatusCode.ALREADY_EXISTS, message)


class UserDoesNotExist(DbConnectionError):
    def __init__(self, username, *, message=None):
        if not message:
            message = f'DB entry for user "{username}" does not exist.'
        super().__init__(StatusCode.NOT_FOUND, message)


class WrongCredentials(DbConnectionError):
    def __init__(self, username, *, message=None):
        if not message:
            message = f'Invalid password provided for user "{username}".'
        super().__init__(StatusCode.UNAUTHENTICATED, message)


class PostDoesNotExist(DbConnectionError):
    def __init__(self, post_id, *, message=None):
        if not message:
            message = f"DB entry for post with id {post_id} does not exist."
        super().__init__(StatusCode.NOT_FOUND, message)


class InvalidJsonString(DbConnectionError):
    def __init__(self, json_string, *, message=None):
        if not message:
            message = f"Invalid json string: {json_string}"
        super().__init__(StatusCode.INVALID_ARGUMENT, message)


CONNECTION_STRING = (
    "postgresql+psycopg2://{db_username}:{db_password}@db:5432/{db_name}"
)


class DbConnection:
    def __init__(self, db_username: str, db_password: str, db_name: str):

        self._engine = create_engine(
            CONNECTION_STRING.format(
                db_username=db_username, db_password=db_password, db_name=db_name
            ),
            future=True,
        )
        self._Session = sessionmaker(bind=self._engine)
        # Initializes db only when db is not initialized
        Base.metadata.create_all(self._engine)

    def validate_user_credentals(self, username, password):
        with self._Session() as session:
            user = self._find_user(username, session)
            if not self._is_password_correct(password, user.password_hash):
                raise WrongCredentials(username)

    def _find_user(self, username, session_context):
        user = session_context.query(User).filter_by(username=username).first()
        if user is None:
            raise UserDoesNotExist(username)
        return user

    def _is_password_correct(self, password: str, password_hash: str):
        return bcrypt.checkpw(password.encode(), password_hash.encode())

    def create_post(self, author: str, title: str, content: str):
        with self._Session() as session:
            user = self._find_user(author, session)

            post = Post(
                title=title,
                author=user.username,
                content=content,
            )

            session.add(post)
            session.commit()

    def _validate_json(self, json_string):
        try:
            json.loads(json_string)
        except ValueError:
            raise InvalidJsonString(json_string)

    def get_post(self, id):
        with self._Session() as session:
            post = self._find_post(id, session)
            return post

    def _find_post(self, id, session_context):
        post = session_context.query(Post).filter_by(id=id).first()
        if post is None:
            raise PostDoesNotExist(id)
        return post

    def modify_post(self, id, title, content, classification):
        with self._Session() as session:

            post = self._find_post(id, session)

            if title and title != post.title:
                post.title = title
            if content and content != post.content:
                post.content = content
                post.tagged_at = None
                post.classification = None
            if classification and classification != post.classification:
                self._validate_json(classification)
                # self.tagged_at todo
                post.classification = classification

            session.commit()

    # def remove_post(self, id):
    #     with self._Session() as session:
    #         post = self._find_post(id, session)
    #         session.delete(post)
    #         session.commit()

    def get_posts(self):
        with self._Session() as session:
            return session.query(Post).all()

    """ Administrative db operations """

    def add_user(self, username, password):
        with self._Session() as session:
            try:
                self._find_user(username, session)
            except UserDoesNotExist:
                password_hash = self._hash_password(password)
                session.add(User(username=username, password_hash=password_hash))
                session.commit()
                return
            raise UserAlreadyExists(username)

    def _hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password.decode("utf8")

    def remove_user(self, username):
        with self._Session() as session:
            user = self._find_user(username, session)
            session.delete(user)
            session.commit()
