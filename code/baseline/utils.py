import json

CLASS_MAP = {
    cn: i for i, cn in enumerate(["Strength", "Weakness", "Todo", "Structure", "Recap", "Other"])
}
iCLASS_MAP = {
    v: k for k, v in CLASS_MAP.items()
}

# converts the sequence of reviews with sentences to just the sentences. The "sid" field is composed of the review id and the sentence number to be reversable
def to_context_free_format(path):
    with open(path, "r") as f:
        d = json.load(f)

    res = []
    for i in d:
        for c, s in enumerate(i["sentences"]):
            k = {"sid": i["id"] + "@" + str(c), "txt": s}
            if "labels" in i:
                k["label"] = i["labels"][c]

            res += [k]

    return res

# converts the given predictions on sentence level back to review-level predictions
def predictions_to_evaluation_format(pred):
    res = {}
    for i in pred:
        iid, six = tuple(i["sid"].split("@"))
        res[iid] = res.get(iid, {})
        res[iid][int(six)] = i["label"]

    return [{"id": k, "labels": [v[j] for j in range(len(v))]} for k, v in res.items()]
