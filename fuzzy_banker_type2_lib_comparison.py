import argparse

import numpy as np
import skfuzzy as fuzz

from controller.loader import load_input_mfs, load_output_mfs, load_rules
from method.defuzzifier_type2 import Type2Defuzzifier
from method.fuzzifier import Fuzzifier
from method.inference import InferenceEngine
from model.problem import DecisionProblem

DECISIONS = [
    ("h1", "Loan amount"),
    ("h2", "Monthly payment"),
    ("h3", "Loan term"),
]


def compute_custom_t2(obs, key, input_mfs, output_mfs, rules_json):
    problem = DecisionProblem(input_mfs, output_mfs, rules_json)
    fuzzifier = Fuzzifier(input_mfs)
    defuzz2 = Type2Defuzzifier(output_mfs)
    rs = problem.get_rules(key)
    fr = fuzzifier.fuzzify_for_rules(obs, rs)
    out_deg = InferenceEngine(rs).infer(fr)
    return defuzz2.defuzzify(out_deg, key), out_deg


def generate_xs(output_mfs, key, count=1001):
    pts = output_mfs[key]
    lo = min(x for info in pts.values() for x, _ in info["points"])
    hi = max(x for info in pts.values() for x, _ in info["points"])
    return np.linspace(lo, hi, count)


def compute_library_t2(out_deg, xs, output_mfs, key):
    info = output_mfs[key]
    μ_sum_full = np.zeros_like(xs)
    for lbl, α in out_deg.items():
        if α <= 0:
            continue
        pts = [x for x, _ in info[lbl]["points"]]
        mf = fuzz.trapmf(xs, pts) if info[lbl]["type"] == "trapezoid" else fuzz.trimf(xs, pts)
        μ_sum_full += α * mf

    mask = μ_sum_full > 0
    if not mask.any():
        return 0.0
    last = np.where(mask)[0].max()
    xs_trunc = xs[: last + 1]
    μ_sum_trunc = μ_sum_full[: last + 1]

    return fuzz.defuzz(xs_trunc, μ_sum_trunc, 'centroid')


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--inflow", type=float, required=True)
    p.add_argument("--income_sum", type=float, required=True)
    p.add_argument("--dependents", type=float, required=True)
    p.add_argument("--age", type=float, required=True)
    args = p.parse_args()
    obs = vars(args)

    input_mfs = load_input_mfs("parameters_config/input_mfs.json")
    output_mfs = load_output_mfs("parameters_config/output_mfs.json")
    rules_json = load_rules("parameters_config/rules.json")

    print(f"{'Key':<4} {'Decision':<20} {'Custom T2':>10} {'Library T2':>12}")
    print("-" * 52)

    for key, title in DECISIONS:
        z_custom, out_deg = compute_custom_t2(obs, key, input_mfs, output_mfs, rules_json)
        xs = generate_xs(output_mfs, key, count=1001)
        z_library = compute_library_t2(out_deg, xs, output_mfs, key)
        print(f"{key:<4} {title:<20} {z_custom:10.2f} {z_library:12.2f}")


if __name__ == "__main__":
    main()
