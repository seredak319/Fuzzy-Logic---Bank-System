from controller.cli_params import CLIParams
from controller.loader import load_input_mfs, load_output_mfs, load_rules
from logger.logger import ResultLogger
from method.defuzzifier_type1 import Type1Defuzzifier
from method.defuzzifier_type2 import Type2Defuzzifier
from method.fuzzifier import Fuzzifier
from method.inference import InferenceEngine
from model.problem import DecisionProblem

DECISIONS = [
    ("h1", "Loan amount"),
    ("h2", "Monthly payment"),
    ("h3", "Loan term")
]


def main():
    args = CLIParams.parse_args()
    obs = {
        "inflow": args.inflow,
        "income_sum": args.income_sum,
        "dependents": args.dependents,
        "age": args.age
    }

    logger = ResultLogger()
    logger.log_params(obs)

    input_mfs = load_input_mfs("parameters_config/input_mfs.json")
    output_mfs = load_output_mfs("parameters_config/output_mfs.json")
    rules = load_rules("parameters_config/rules.json")

    logger.log_config_loaded([
        "parameters_config/input_mfs.json",
        "parameters_config/output_mfs.json",
        "parameters_config/rules.json"
    ])

    fuzzifier = Fuzzifier(input_mfs)
    problem = DecisionProblem(input_mfs, output_mfs, rules)
    defuzz1 = Type1Defuzzifier(output_mfs)
    defuzz2 = Type2Defuzzifier(output_mfs)

    full_m = {
        f"{var}.{lbl}": fuzzifier._interp(obs[var], info["points"])
        for var, mfs in input_mfs.items()
        for lbl, info in mfs.items()
    }
    full_m = dict(sorted(full_m.items()))
    print(f"{'Variable.Label':<20} {'Degree':>8}")
    print("-" * 29)
    logger.log_params_nf(full_m)
    for name, deg in full_m.items():
        print(f"{name:<20} {deg:8.2f}")
    print()

    results = []
    for key, title in DECISIONS:
        rs = problem.get_rules(key)
        fr = fuzzifier.fuzzify_for_rules(obs, rs)
        ie = InferenceEngine(rs)
        out_deg = ie.infer(fr)
        flat = dict(sorted({f"{key}.{lbl}": deg for lbl, deg in out_deg.items()}.items()))
        logger.log_params(flat)

        print(f"Output memberships for {title}:")
        print(f"{'Label':<15} {'Degree':>8}")
        print("-" * 24)
        for lbl, deg in flat.items():
            label = lbl.split(".", 1)[1]
            print(f"{label:<15} {deg:8.2f}")
        print()

        z1 = defuzz1.defuzzify(out_deg, key)
        z2 = defuzz2.defuzzify(out_deg, key)
        logger.log_decision_result(title, z1, z2)
        results.append((key, title, z1, z2))

    print(f"{'Key':<4} {'Decision':<20} {'Type-1':>10} {'Type-2':>10}")
    print("-" * 50)
    for key, title, z1, z2 in results:
        print(f"{key:<4} {title:<20} {z1:10.2f} {z2:10.2f}")

    print(f"\nResults logged to {logger.path}")


if __name__ == "__main__":
    main()
