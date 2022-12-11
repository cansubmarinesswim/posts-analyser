from pathlib import Path
from typing import List, Tuple

from flask import Flask, jsonify, request
from healthcheck import HealthCheck
import numpy as np
from scipy.special import softmax

import posts_sentiment_analyser.model_utils as model_utils

try:
    from posts_sentiment_analyser.model_dir import model_dir
except ModuleNotFoundError:
    raise ModuleNotFoundError("Run setup.py first to fetch model components.")

model_dir = Path(model_dir)
for component in ("tokenizer", "model", "labels.txt"):
    if not (model_dir / component).exists():
        raise FileNotFoundError(f"{model_dir / component} not found. Run setup.py first to download model components.")

tokenizer = model_utils.load_tokenizer(f"{model_dir / 'tokenizer'}")
model = model_utils.load_model(f"{model_dir / 'model'}")
labels = model_utils.load_labels(f"{model_dir / 'labels.txt'}")

def _classify(text: str) -> List[Tuple[str, str]]:
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    ranking = np.argsort(scores)[::-1]
    sort_by_ranking = lambda x_list: [x for _, x in sorted(zip(ranking, x_list), key=lambda x: x[0])]
    
    return [(label, str(round(score, 4))) for (label, score) in zip(
        sort_by_ranking(labels), 
        sort_by_ranking(scores)
    )]

app = Flask(__name__)

health = HealthCheck()

def classify_works():
    try:
        _ = _classify("Input text")[0][0]
        return True, "healthy"
    except:
        return False, "service is broken"

health.add_check(classify_works)

@app.route('/healthcheck', methods=['GET', 'POST'])
def healthcheck():
    return health.run()

@app.route('/classify', methods=['POST'])
def classify():
    if request.method == 'POST':
        text = request.form['text']
        out = _classify(text)
        return jsonify(out)

def create_app():
    return app