from typing import Dict, Any, List

class Rule:
    def __init__(self, antecedent: Dict[str, Any], consequent: Dict[str, str]):
        self.antecedent = antecedent
        self.consequent = consequent

    def applies_to(self, decision: str) -> bool:
        return decision in self.consequent

class DecisionProblem:
    def __init__(self,
                 input_mfs: Dict[str, Any],
                 output_mfs: Dict[str, Any],
                 rules_json: List[Dict[str, Any]]):
        self.input_mfs = input_mfs
        self.output_mfs = output_mfs
        self.rules = [Rule(r['if'], r['then']) for r in rules_json]

    def get_rules(self, decision: str) -> List[Rule]:
        return [rule for rule in self.rules if rule.applies_to(decision)]
