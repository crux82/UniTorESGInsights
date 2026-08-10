import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def predict_with_model(texts, bundle):
    model = bundle["model"]
    tokenizer = bundle["tokenizer"]
    labels = bundle["labels"]

    enc = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=200,
        return_tensors="pt"
    )

    input_ids = enc["input_ids"].to(device)
    mask = enc["attention_mask"].to(device)

    with torch.no_grad():
        logits, _ = model(input_ids, mask)

        preds = torch.argmax(logits, dim=1)

        return [labels[p] for p in preds.cpu().tolist()]

def predict_with_sdg_model(texts, bundle):
    """
    Multilabel-trained model but we pick the single label with the
    highest sigmoid probability for each text (argmax strategy).
    Returns e.g. ["13", "7", "1", ...] — SDG numbers as strings.
    """
    model = bundle["model"]
    tokenizer = bundle["tokenizer"]
    labels = bundle["labels"]

    enc = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=200,
        return_tensors="pt"
    )

    input_ids = enc["input_ids"].to(device)
    mask = enc["attention_mask"].to(device)

    with torch.no_grad():
        logits = model(input_ids, mask)               # raw logits, shape (B, 17)
        probs = torch.sigmoid(logits)                 # sigmoid → probabilities
        best_idx = torch.argmax(probs, dim=1)         # index of highest prob per sample

    return [labels[i] for i in best_idx.cpu().tolist()]

def predict(texts, bundle):
    """Route to the correct prediction function based on model type."""
    if bundle.get("is_sdg", False):
        return predict_with_sdg_model(texts, bundle)
    else:
        return predict_with_model(texts, bundle)