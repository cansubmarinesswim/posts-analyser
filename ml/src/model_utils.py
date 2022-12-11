from pathlib import Path
from typing import List

from transformers import AutoModelForSequenceClassification, AutoTokenizer
import urllib.request

def load_tokenizer(source: str) -> AutoTokenizer:
    '''
    Load and return transformers.AutoTokenizer

            Parameters:
                    source (str): Storage path to saved model or model name to download pretrained model through transformers module.

            Returns:
                    tokenizer (AutoTokenizer): Transformers object
    '''
    return AutoTokenizer.from_pretrained(source)


def load_model(source: str, save_path: str = None) -> AutoModelForSequenceClassification:
    '''
    Load and return transformers.AutoModelForSequenceClassification

            Parameters:
                    source (str): Storage path to saved model or model name to download pretrained model through transformers module.
                    save_path (str): If provided, model will be saved locally.

            Returns:
                    model (AutoModelForSequenceClassification): Transformers object
    '''
    model = AutoModelForSequenceClassification.from_pretrained(source)

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(save_path)

    return model

def load_labels(source: str) -> List[str]:
    '''
    Load and return a list of label names.

            Parameters:
                    source (str): Storage path or URL link.

            Returns:
                    labels (List[str]): Label names list in the order enabling mapping.
    '''
    if Path(source).is_file():
        with open(source) as f:
            lines = [l.strip() for l in f.readlines()]
    else:
        with urllib.request.urlopen(source) as f:
            lines = f.read().decode('utf-8').split("\n")
    
    lines = map(lambda x: x.split('\t'), lines)
    lines = filter(lambda x: len(x) > 1, lines)
    labels = [line[1] for line in lines]
    return labels