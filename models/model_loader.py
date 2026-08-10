import os
import json
import torch

from transformers import AutoTokenizer, BertTokenizer
from huggingface_hub import snapshot_download

from models.classifier import Classifier
from models.sdg_classifier import BERTClassifier

from configs.sdg_labels import SDG_LABELS
from configs.model_config import MODEL_FOLDERS


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# MODEL PATHS
BASE_PATH = "./models/"

# LOAD MODEL FROM FOLDER  (original models)
def load_model_from_folder(folder_path):

    # CONFIG
    with open(os.path.join(folder_path, "config.json")) as f:
        config = json.load(f)

    model_name = config["model_name"]
    dropout = config.get("dropout_rate", 0.1)

    # LABELS (always normal classification)
    with open(os.path.join(folder_path, "labels.json")) as f:
        label_data = json.load(f)

    labels = label_data["label_list"]
    num_labels = len(labels)

    # TOKENIZER
    tokenizer = AutoTokenizer.from_pretrained(folder_path)

    # MODEL
    model = Classifier(model_name, num_labels, dropout)

    # WEIGHTS
    state = torch.load(os.path.join(folder_path, "model.pt"), map_location=device)

    model.load_state_dict(state, strict=True)
    model.to(device)
    model.eval()

    return {
        "model": model,
        "tokenizer": tokenizer,
        "labels": labels,
        "config": config
    }


def load_sdg_model_from_folder(folder_path):

    # CONFIG
    with open(os.path.join(folder_path, "config.json")) as f:
        config = json.load(f)

    dropout = config.get("dropout_rate", 0.1)
    num_classes = config["num_classes"]           # 17

    # LABEL MAP  {"0": "1", "1": "2", ..., "16": "17"}
    with open(os.path.join(folder_path, "label_map.json")) as f:
        label_map = json.load(f)

    # Convert to ordered list by integer key → ["1", "2", ..., "17"]
    raw_labels = [label_map[str(i)] for i in range(num_classes)]
    pretty_labels = [SDG_LABELS[x] for x in raw_labels]

    # TOKENIZER  (saved inside a 'tokenizer' subfolder)
    tokenizer_path = os.path.join(folder_path, "tokenizer")
    tokenizer = BertTokenizer.from_pretrained(tokenizer_path)

    # MODEL
    model = BERTClassifier(n_classes=num_classes, dropout_rate=dropout)

    # WEIGHTS
    state = torch.load(os.path.join(folder_path, "model_state.pt"), map_location=device)
    model.load_state_dict(state, strict=True)
    model.to(device)
    model.eval()

    return {
        "model": model,
        "tokenizer": tokenizer,
        "labels": raw_labels, # for prediction logic
        "pretty_labels": pretty_labels, # for charts/UI
        "config": config,
        "is_sdg": True        # flag so prediction knows which path to take
    }

# MODEL CACHE
LOADED_MODELS = {}

def get_model(task_name):

    if task_name in LOADED_MODELS:
        return LOADED_MODELS[task_name]

    repo = f"sag-uniroma2/{MODEL_FOLDERS[task_name]}"
    folder = snapshot_download(repo_id=repo)

    if task_name == "17 SDG Alignment":
        bundle = load_sdg_model_from_folder(folder)
    else:
        bundle = load_model_from_folder(folder)

    LOADED_MODELS[task_name] = bundle
    return bundle
