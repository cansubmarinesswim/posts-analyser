from flask import Flask, jsonify, request
from healthcheck import HealthCheck
from gateway.ml_connector import MlConnector, MlConnectorError
from gateway.db_controller_connector import DbConnector

app = Flask(__name__)

ml_connector = MlConnector(service_host="0.0.0.0", service_port="60053")
db_connector = DbConnector()

health = HealthCheck()

def classify_works():
    try:
        return True, "healthy"
    except:
        return False, "service is broken"

health.add_check(classify_works)

@app.route('/healthcheck', methods=['GET', 'POST'])
def healthcheck():
    return health.run()

@app.route('/post/create', methods=['POST'])
def create_post():
    try:
        post_content =request.form.get("post")
        classification = ml_connector.classify_post(post_content)
        # zapisz w bazie
        # Dostań ID postu nowego w bazie
        id = 10

        return jsonify({"post_id": id, "classification": classification}), 200
    except MlConnectorError as e:
        print("MlConnectorError: ", e)
        return jsonify(success=False), e.status_code
    except:
        return jsonify(success=False), 400

@app.route('/post/<id>', methods=['GET'])
def remove_post(id):
    try:
        # Spytaj baze o usuniecie
        # Dostan info o usunieciu
        out = {"post_id": id}
        return jsonify(out), 200
    except:
        return jsonify("Failed"), 400

@app.route('/posts', methods=['GET'])
def read_posts():
    try:
        # Spytaj baze o posty
        # sformatuj je do zakldanego formtu json
        out = {
            "posts": [
                {"id": 1},
                {"id": 2}
            ]
        }
        return jsonify(out)
    except:
        return jsonify("Failed"), 400

def create_app():
    return app

create_app()