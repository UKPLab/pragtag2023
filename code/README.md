## Starting Kit for PragTag Shared Task 2023

In this starting kit you can find the evaluation scripts used in codalab, and a baseline script for fine-tuning a RoBERTa model for the task and outputting predictions in the desired format.

### evaluation
The evaluation scripts. Use the main.py to run evaluation on your model output. If anything fails locally, it will also fail on the server, so use this script for debugging.

```bash
python3 main.py <input_path> <output_path>

```

Here, the input path should point to a directory containing a folder "ref" with the true labels (or training data with labels) under the name `test_labels.json`, and a folder res with the predicted labels (under `predicted.json`).

Feel free to use the eval.py or load.py methods to integrate the evaluation into your validation/dev process. 

### baseline

This folder contains the code for finetuning a RoBERTa model and code for using it for prediction. Note that this baseline neglects all context of a sentence and predicts a label in isolation.

Just run for finetuning

```bash
python3 finetune_baseline.py <train data path> <output path>
```

For prediction

```bash
python3 predict_baseline.py <test input data path> <model checkpoint path> <output path>
```

### Submission_zero.zip

Example submission file that you can upload to the sandbox phase to understand the submission process.


### Troubleshooting Codalab

Sometimes codalab fails for uploads despite correct formatting of the files. If you cannot find the error, try re-running the submission. Note that the submission file zip should not contain any folders, i.e. the predictions JSON should be on the first level after unzipping the file.

### Auxiliary Data

Click on the link provided in the shared task and request the data. After confirmation (requires prior registration with the shared task), you will receive the auxiliary data. For conveniently loading it, checkout the associated (github repo)[https://github.com/UKPLab/nlpeer].
