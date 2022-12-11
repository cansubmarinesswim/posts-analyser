from flask import Flask, jsonify, request
from healthcheck import HealthCheck


app = Flask(__name__)

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

        # spytaj ML
        # Dostan odpowiedz od ML
        # zapisz w bazie
        # Dostań ID postu nowego w bazie
        id = 10

        return jsonify({"post_id": id}), 200
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