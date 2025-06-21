from typing import Dict, List

class Label:
    def __init__(self, name: str, mf_type: str, params: List[float]):
        self.name = name
        self.mf_type = mf_type
        self.params = params

class Variable:
    def __init__(self, name: str, labels: Dict[str, Label]):
        self.name = name
        self.labels = labels

class Rule:
    def __init__(self, antecedents: List[Dict], consequent: Dict):
        self.antecedents = antecedents
        self.consequent = consequent

class Example:
    def __init__(self, id: str, inputs: Dict[str, float], decision: str):
        self.id = id
        self.inputs = inputs
        self.decision = decision

class RepresentativeSet:
    def __init__(self, output_values: Dict[str, Dict[str, float]], examples: List[Example]):
        self.output_values = output_values
        self.examples = examples