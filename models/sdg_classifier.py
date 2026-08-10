import torch.nn as nn
from transformers import BertModel

# SDG CLASSIFIER
class BERTClassifier(nn.Module):
    """SDG-specific classifier: trained multilabel but predicts via argmax (best label)."""

    def __init__(self, n_classes, dropout_rate=0.1):
        super(BERTClassifier, self).__init__()
        self.transformer = BertModel.from_pretrained('bert-base-cased')
        self.drop = nn.Dropout(p=dropout_rate)
        self.linear = nn.Linear(
            in_features=self.transformer.config.hidden_size,
            out_features=n_classes
        )

    def forward(self, input_ids, attention_mask):
        output = self.transformer(
            input_ids=input_ids,
            attention_mask=attention_mask,
            return_dict=True
        ).pooler_output

        output = self.drop(output)
        output = self.linear(output)

        return output