import sys
import random

import numpy as np
import torch

from datasets import Dataset
from transformers import AutoTokenizer, TrainingArguments, Trainer
from transformers import AutoModelForSequenceClassification

from utils import CLASS_MAP, to_context_free_format

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print("TRAINING on ", device)

seed = 42
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

# training data
train_data_path = sys.argv[1]


def preprocess(item):
    item["label"] = torch.tensor(CLASS_MAP[item["label"]]).unsqueeze(0)

    return item


# tokenizer
tokenizer = AutoTokenizer.from_pretrained("roberta-base")


def tokenize(examples):
    toks = tokenizer.batch_encode_plus(examples["txt"], padding="max_length", max_length=512, truncation=True,
                                       return_tensors="pt")
    toks["labels"] = examples["label"]

    return toks


full_data = Dataset.from_list(to_context_free_format(train_data_path)) \
    .map(preprocess) \
    .shuffle(seed=seed) \
    .train_test_split(test_size=0.2) \
    .map(tokenize, batched=True)

# model
model = AutoModelForSequenceClassification.from_pretrained("roberta-base", num_labels=len(CLASS_MAP))

# fine-tuning
training_args = TrainingArguments(
    output_dir=sys.argv[2] + '/results',
    num_train_epochs=20,
    learning_rate=1e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir=sys.argv[2] + '/logs',
    logging_steps=10,
    evaluation_strategy='steps',
    save_total_limit=5,
    load_best_model_at_end=True,
    greater_is_better=True
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=full_data["train"],
    eval_dataset=full_data["test"],
    tokenizer=tokenizer,
)

# actual training
trainer.train()

# loading for prediction
best_path = sys.argv[2] + '/results/best_roberta'
trainer.save_model(best_path)

print("Done")
