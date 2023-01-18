from flask import Flask, jsonify, request
from healthcheck import HealthCheck
from gateway.ml_connector import MlConnector, MlConnectorError
from gateway.db_controller_connector import DbConnector, DbConnectorError
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

ml_connector = MlConnector(host="ml", port="60053")
db_connector = DbConnector(host="db_controller_service", port="60052")

fetched_posts_counter = Counter("fetched_posts", "How many times db has been queried for posts")
created_posts_counter = Counter("created_posts", "How many posts have been created")
deleted_posts_counter = Counter("deleted_posts", "How many posts been deleted")
failed_requests = Counter("failed_requests", "How many requests raised exception")

health = HealthCheck()


def classify_works():
    try:
        return True, "healthy"
    except:
        return False, "service is broken"


health.add_check(classify_works)


@app.route("/api/healthcheck", methods=["GET", "POST"])
def healthcheck():
    return health.run()

@app.route('/metrics')
def metrics():
    return generate_latest()


@app.route("/api/post/create", methods=["POST"])
@failed_requests.count_exceptions()
def create_post():
    try:
        username = request.form.get("username")
        post_title = request.form.get("title")
        post_content = request.form.get("post")

        classification = ml_connector.classify_post(post_content)
        db_connector.add_post(
            author=username,
            title=post_title,
            content=post_content,
            classification=classification,
        )
        created_posts_counter.inc()

        return jsonify(success=True), 200
    except MlConnectorError as e:
        print("MlConnectorError: ", e.message)
        return jsonify(success=False), e.status_code
    except DbConnectorError as e:
        print("DbConnectorError: ", e.message)
        return jsonify(success=False), e.status_code
    except:
        return jsonify(success=False), 400


@app.route("/api/post/add_user", methods=["POST"])
@failed_requests.count_exceptions()
def add_user():
    try:
        username = request.form.get("username")
        password = request.form.get("password")

        db_connector.add_user(
            username=username,
            password=password,
        )

        return jsonify(success=True), 200
    except DbConnectorError as e:
        print("DbConnectorError: ", e.message)
        return jsonify(success=False), e.status_code
    except:
        return jsonify(success=False), 400


@app.route("/api/post/<id>", methods=["DELETE"])
@failed_requests.count_exceptions()
def remove_post(id):
    try:
        db_connector.remove_post(int(id))
        deleted_posts_counter.inc(())
        return jsonify(success=True), 200
    except DbConnectorError as e:
        print("DbConnectorError: ", e.message)
        return jsonify(success=False), e.status_code
    except:
        return jsonify("Failed"), 400


@app.route("/api/posts", methods=["GET"])
@failed_requests.count_exceptions()
def read_posts():
    try:
        posts = db_connector.get_posts()
        fetched_posts_counter.inc()
        return jsonify(posts), 200
    except:
        return jsonify("Failed"), 400


def create_app():
    return app


create_app()
