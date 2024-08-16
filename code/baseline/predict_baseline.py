import json
import random
import sys

import numpy as np
import torch
from datasets import Dataset
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from utils import to_context_free_format, CLASS_MAP, iCLASS_MAP, predictions_to_evaluation_format

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print("EVALUATING on ", device)

seed=42
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

best_model_path = sys.argv[2]
best_model = AutoModelForSequenceClassification.from_pretrained(best_model_path)
best_model.eval()
best_model.to(device)
best_tok = AutoTokenizer.from_pretrained(best_model_path)


def preprocess(item):
    if "label" in item:
        item["label"] = torch.tensor(CLASS_MAP[item["label"]]).unsqueeze(0)

    return item


def tokenize(examples):
    toks = best_tok.batch_encode_plus(examples["txt"], padding="max_length", max_length=512, truncation=True, return_tensors="pt")

    return toks


eval_data_path = sys.argv[1]
eval_data = Dataset.from_list(to_context_free_format(eval_data_path))\
    .map(preprocess)\
    .map(tokenize, batched=True)

batch_size = 2
inputs = DataLoader(eval_data, batch_size=batch_size)

predictions = []
for batch_inputs in tqdm(inputs, desc="Iterating over input"):
    batch_outputs = best_model(input_ids = torch.stack(batch_inputs["input_ids"]).transpose(1,0).to(device),
                          attention_mask=torch.stack(batch_inputs["attention_mask"]).transpose(1,0).to(device))
    batch_predictions = torch.argmax(batch_outputs.logits, dim=1)

    predictions += [{"sid": batch_inputs["sid"][i], "label": iCLASS_MAP[batch_predictions[i].item()]} for i in range(batch_size)]


r = predictions_to_evaluation_format(predictions)
with open(sys.argv[3] + "/predicted.json", "w+") as f:
    json.dump(r, f, indent=4)

print("Done")
