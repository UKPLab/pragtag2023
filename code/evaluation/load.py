import json
import os

LABELS = {
    "Structure",
    "Recap",
    "Todo",
    "Strength",
    "Weakness",
    "Other"
}

# loads labelled data (aka test reference labels or prediction labels)
def load_labelled_data(path):
    def validation(data):
        return validate_json_format(data, check_input=False, check_output=True)

    return load_data(path, validation)

# loads input data (aka test input without labels)
def load_input_data(path):
    def validation(data):
        return validate_json_format(data, check_input=True, check_output=False)

    return load_data(path, validation)

# loads training data (aka data with input and labels)
def load_train_data(path):
    def validation(data):
        return validate_json_format(data, check_input=True, check_output=True)

    return load_data(path, validation)

# loads the data given a path; validation is performed using the provided validation function
def load_data(path, validation):
    if not os.path.exists(path) or not os.path.isfile(path) or not path.endswith(".json"):
        print("ERROR: Provided file path does not point to a .json file or may not exist")
        raise ValueError("Invalid file path provided")

    try:
        with open(path, "r") as file:
            data = json.load(file)

        validation(data)
    except UnicodeDecodeError as e:
        print("ERROR: Cannot load provided file as a unicode-encoded json.", e)
        raise e
    except json.decoder.JSONDecodeError as e:
        print("ERROR: Cannot load provided file as json -- invalid formatting.", e)
        raise e
    except AssertionError as e:
        print("ERROR: Provided json is not formatted according to the task requirements", e)
        raise e

    return {p["id"]: p for p in data}

# validates the given output/input file
def validate_json_format(data, check_input, check_output):
    assert type(data) == list and len(data) , "the data file should contain a list of objects"

    ids = []
    for i, o in enumerate(data):
        for req in ["id"] + (["labels"] if check_output else []) + (["sentences"] if check_input else []):
            assert req in o, f"item at list position {i} is lacking the required '{req}' field"

        if check_output:
            assert len(list(filter(lambda l: l not in LABELS, o["labels"]))) == 0, f"item at list position {i} uses an " \
                                                                                   f"unknown label. Only {str(LABELS)} " \
                                                                                   f"are permitted."

        if check_input:
            assert all([type(s) == str for s in o["sentences"]]) and len(o["sentences"]) > 0, f"invalid input at {i}. Expecting >0 strings."

        if check_input and check_output:
            assert len(o["sentences"]) == len(o["labels"]), f"number of sentences and labels invalid at {i}. Should be the same."

        ids += [o["id"]]

    assert len(set(ids)) == len(ids), "ids need to be unique -- found a duplicate one"

    return True

# validates that prediction and gold file align
def validate_prediction_against_gold(pred, gold):
    # check same ids
    assert set(pred.keys()) == set(gold.keys()), "gold data and prediction review report ids are " \
                                                                     "not identical"

    # check labels per item
    for gid, g in gold.items():
        p = pred[gid]

        assert len(p["labels"]) == len(g["labels"]), f"Label count for review report {gid} is inconsistent between " \
                                                     f"gold data and predictions."

    return True

# use this method to load gold and prediction data for evaluation
def load_prediction_and_gold(path_pred, path_gold):
    try:
        pred = load_labelled_data(path_pred)
    except Exception as e:
        print("Failed to load predictions", e)
        raise ValueError("Invalid prediction file")

    try:
        gold = load_labelled_data(path_gold)
    except Exception as e:
        print("Failed to load gold data", e)
        raise ValueError("Invalid gold data file")

    try:
        validate_prediction_against_gold(pred, gold)
    except Exception as e:
        print("Gold data and predictions are not compatible", e)
        raise ValueError("Invalid prediction file")

    return pred, gold

