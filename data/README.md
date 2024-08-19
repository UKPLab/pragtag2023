# PragTag-2023 Shared Task: Data

The PragTag shared task uses the F1000RD annotated samples plus a newly created secret share of COLING-20 data annotated with pragmatic tags (called "secret" in the dataset).

## JSON Format

All json files follow the same format:

```json
[
 {
        "id": "<review-report-id-in-nlpeer>",
        "sentences": [
            "This is a sentence.",
            "This is another sentence!",
            "This yet another sentence."
        ],
        "pid": "<paper-id-in-nlpeer>",
        "domain": "<domain tag in F1000RD or 'secret'>"
    },
    ...
]
```


## Structure

The data is given in the following structure according to the test conditions of the shared task.

```
public_main = contains training data and test inputs for the main conditions
secret_main = contains the test inputs for the secret condition and all others
reference_main = contains the labels for the samples of the main conditions
reference_secret = contains the labels for the samples of the secret conditions
```
