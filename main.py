# main.py
from controller.cli_params import CLIParams
from controller.loader import load_input_mfs, load_output_mfs, load_rules
from logger.logger import ResultLogger


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
    cfg_input = "parameters_config/input_mfs.json"
    cfg_output = "parameters_config/output_mfs.json"
    cfg_rules = "parameters_config/rules.json"
    input_mfs = load_input_mfs(cfg_input)
    output_mfs = load_output_mfs(cfg_output)
    rules = load_rules(cfg_rules)
    logger.log_config_loaded([cfg_input, cfg_output, cfg_rules])
    for decision in ("h1", "h2", "h3"):
        logger.log_decision_start(decision)
        result_t1 = "<Type-1 result>"
        result_t2 = "<Type-2 result>"
        logger.log_decision_result(decision, result_t1, result_t2)
    print(f"Results logged to {logger.path}")


if __name__ == "__main__":
    main()
