import argparse
from os.path import join as pjoin

from eval import eval_across_domains
from load import load_prediction_and_gold


def main(pred_path, gold_path, out_path):
    pred, gold = load_prediction_and_gold(pred_path, gold_path)

    per_domain, mean = eval_across_domains(gold, pred)

    with open(out_path, "w+") as f:
        for k, v in per_domain.items():
            f.write(f"f1_{k}:{v}\n")
        f.write(f"f1_mean:{mean}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate predictions on gold data')
    parser.add_argument('input', type=str, help='directory of the predictions and gold labels')
    parser.add_argument('output', type=str, help='path to the output file')

    args = parser.parse_args()

    inpath = args.input
    outpath = args.output

    main(pjoin(inpath, "res", "predicted.json"), pjoin(inpath, "ref", "test_labels.json"), pjoin(outpath, "scores.txt"))
