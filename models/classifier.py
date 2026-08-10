import torch
import torch.nn as nn
from transformers import AutoModel, AutoConfig

# CLASSIFIER (original - used by all models EXCEPT SDG)
class Classifier(nn.Module):
    def __init__(self, model_name, num_labels, dropout_rate):
        super().__init__()

        self.encoder = AutoModel.from_pretrained(model_name)
        config = AutoConfig.from_pretrained(model_name)

        self.cls_size = config.hidden_size
        self.dropout = nn.Dropout(dropout_rate)
        self.fc = nn.Linear(self.cls_size, num_labels)

    def forward(self, input_ids, attention_mask):
        outputs = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        token_embeddings = outputs.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()

        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, dim=1)
        sum_mask = torch.clamp(input_mask_expanded.sum(dim=1), min=1e-9)
        cls = sum_embeddings / sum_mask

        cls = self.dropout(cls)
        logits = self.fc(cls)

        return logits, cls