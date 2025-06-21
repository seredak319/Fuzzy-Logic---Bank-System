from controller.cli_params      import CLIParams
from controller.loader          import load_input_mfs, load_output_mfs, load_rules
from logger.logger              import ResultLogger
from method.defuzzifier_type1 import Type1Defuzzifier
from model.problem              import DecisionProblem
from method.fuzzifier           import Fuzzifier
from method.inference           import InferenceEngine

def main():
    args = CLIParams.parse_args()
    obs = {
        "inflow":     args.inflow,
        "income_sum": args.income_sum,
        "dependents": args.dependents,
        "age":        args.age
    }

    logger = ResultLogger()
    logger.log_params(obs)

    cfg_i = "parameters_config/input_mfs.json"
    cfg_o = "parameters_config/output_mfs.json"
    cfg_r = "parameters_config/rules.json"

    input_mfs  = load_input_mfs(cfg_i)
    output_mfs = load_output_mfs(cfg_o)
    rules      = load_rules(cfg_r)

    logger.log_config_loaded([cfg_i, cfg_o, cfg_r])

    problem    = DecisionProblem(input_mfs, output_mfs, rules)
    fuzzifier  = Fuzzifier(input_mfs)
    defuzz1    = Type1Defuzzifier(output_mfs)

    for h in ("h1", "h2", "h3"):
        logger.log_decision_start(h)

        rs      = problem.get_rules(h)
        fr      = fuzzifier.fuzzify_for_rules(obs, rs)
        ie      = InferenceEngine(rs)
        out_deg = ie.infer(fr)

        logger.log_params({f"{h}.{lbl}": deg for lbl, deg in out_deg.items()})

        z1 = defuzz1.defuzzify(out_deg, h)
        logger.log_decision_result(h, z1, "<Type-2 pending>")

    print(f"Results logged to {logger.path}")

if __name__ == "__main__":
    main()
