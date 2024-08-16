from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import numpy as np
import argparse


# given gold and prediction, compute the f1 macro across reviews
def evaluate(gold, pred):
    rids = list(gold.keys())

    return f1_score([l for r in rids for l in gold[r]["labels"]], [l for r in rids for l in pred[r]["labels"]],
                    average="macro")


# compute the confusion matrix across reviews
def confusion(gold, pred):
    rids = list(gold.keys())

    return confusion_matrix([l for r in rids for l in gold[r]], [l for r in rids for l in pred[r]])


# computes f1 macro for each domains and computes the mean across domains
def eval_across_domains(gold, pred):
    domains = set(g["domain"] for g in gold.values())
    rid_to_domain = {rid : g["domain"] for rid, g in gold.items()}

    per_domain = {d: evaluate(dict(filter(lambda x: x[1]["domain"] == d, gold.items())),
                              dict(filter(lambda x: rid_to_domain[x[1]["id"]] == d, pred.items()))) for d in domains}

    return per_domain, np.mean(list(per_domain.values()))

