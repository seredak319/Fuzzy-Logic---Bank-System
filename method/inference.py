from typing import Dict, Any, List
from model.problem import Rule
from method.fuzzifier import FuzzificationResult

class InferenceEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def infer(self, fuzz_res: FuzzificationResult) -> Dict[str, float]:
        degrees: Dict[str, float] = {}
        for rule in self.rules:
            alpha = self._eval_antecedent(rule.antecedent, fuzz_res)
            label = next(iter(rule.consequent.values()))
            degrees[label] = max(degrees.get(label, 0.0), alpha)
        return degrees

    def _eval_antecedent(self, cond: Any, fuzz_res: FuzzificationResult) -> float:
        if isinstance(cond, dict):
            if "and" in cond:
                return min(self._eval_antecedent(c, fuzz_res) for c in cond["and"])
            if "or" in cond:
                return max(self._eval_antecedent(c, fuzz_res) for c in cond["or"])
            var,label = next(iter(cond.items()))
            return fuzz_res.degree(var, label)
        return 0.0
