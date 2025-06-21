from typing import Dict, List, Any
from model.problem import Rule

class FuzzificationResult:
    def __init__(self, data: Dict[str, Dict[str, float]]): self.data = data
    def degree(self, var: str, label: str) -> float: return self.data[var][label]
    def variables(self) -> List[str]: return list(self.data.keys())
    def labels(self, var: str) -> List[str]: return list(self.data[var].keys())

class Fuzzifier:
    def __init__(self, input_mfs: Dict[str, Dict[str, Any]]): self.input_mfs = input_mfs

    def fuzzify_for_rules(self, obs: Dict[str, float], rules: List[Rule]) -> FuzzificationResult:
        vars = set()
        for r in rules: vars |= self._extract_vars(r.antecedent)
        data = {}
        for v in vars:
            mfs = self.input_mfs[v]
            x = obs[v]
            data[v] = {lbl: self._interp(x, info["points"]) for lbl, info in mfs.items()}
        return FuzzificationResult(data)

    def _extract_vars(self, cond: Any) -> set:
        if isinstance(cond, dict):
            if "and" in cond: return set().union(*(self._extract_vars(c) for c in cond["and"]))
            if "or" in cond: return set().union(*(self._extract_vars(c) for c in cond["or"]))
            return set(cond.keys())
        return set()

    def _interp(self, x: float, pts: List[List[float]]) -> float:
        pts = sorted(pts, key=lambda p: p[0])
        if x <= pts[0][0]: return pts[0][1]
        if x >= pts[-1][0]: return pts[-1][1]
        for i in range(len(pts)-1):
            x0, y0 = pts[i]; x1, y1 = pts[i+1]
            if x0 <= x <= x1:
                if x1 == x0: return max(y0, y1)
                return y0 + (y1-y0)*(x-x0)/(x1-x0)
        return 0.0
