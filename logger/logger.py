# sterowanie/logger.py
import os
import logging
from typing import Dict, Any, Sequence

class ResultLogger:
    def __init__(self, results_dir: str = "results", result_filename: str = "result.txt"):
        os.makedirs(results_dir, exist_ok=True)
        self.path = os.path.join(results_dir, result_filename)
        if os.path.exists(self.path):
            os.remove(self.path)
        logging.basicConfig(
            filename=self.path,
            filemode='w',
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self._log_header()

    def _log_header(self):
        logging.info("=== Fuzzy Credit Decision Results ===")

    def log_params(self, params: Dict[str, Any]):
        logging.info("User input parameters:")
        for k, v in params.items():
            logging.info(f"{k}: {v}")
        logging.info(" ------------------ ")

    def log_config_loaded(self, config_files: Sequence[str]):
        logging.info("Loaded configuration files:")
        for fn in config_files:
            logging.info(fn)

    def log_decision_start(self, decision: str):
        logging.info(f"\n\nComputing decision {decision}\n")

    def log_decision_result(self, decision: str, result_t1: Any, result_t2: Any):
        logging.info(f"{decision} Type-1 result: {result_t1}")
        logging.info(f"{decision} Type-2 result: {result_t2}")
