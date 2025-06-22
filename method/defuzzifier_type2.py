# method/defuzzifier_type2.py

from typing import Dict, List, Any, Tuple


class Type2Defuzzifier:
    def __init__(self, output_mfs: Dict[str, Dict[str, Any]]):
        self.output_mfs = output_mfs

    def defuzzify(self,
                  degrees: Dict[str, float],
                  decision: str) -> float:
        scaled = self.scale_functions(degrees, decision)
        aggregated = self.sum_scaled_functions(scaled)
        regions = self.decompose_regions(aggregated)
        num, den = 0.0, 0.0
        for region in regions:
            h_sr, w = self._centroid_and_weight(region)
            num += h_sr * w
            den += w
        return num / den if den else 0.0

    def scale_functions(self,
                        degrees: Dict[str, float],
                        decision: str
                        ) -> Dict[str, List[List[float]]]:
        scaled = {}
        for label, alpha in degrees.items():
            if alpha <= 0:
                continue
            pts = self.output_mfs[decision][label]['points']
            scaled[label] = [[x, mu * alpha] for x, mu in pts]
        return scaled

    def sum_scaled_functions(self,
                             scaled_mfs: Dict[str, List[List[float]]]
                             ) -> List[List[float]]:
        xs = sorted({x for pts in scaled_mfs.values() for x, _ in pts})
        aggregated = []
        for x in xs:
            mu_sum = sum(self._interp(pts, x) for pts in scaled_mfs.values())
            aggregated.append([x, mu_sum])
        return aggregated

    def decompose_regions(self,
                          aggregated: List[List[float]]
                          ) -> List[Dict[str, Any]]:
        regions = []
        for (x0, y0), (x1, y1) in zip(aggregated, aggregated[1:]):
            if y0 == y1:
                regions.append({
                    'shape': 'rectangle',
                    'h_min': x0,
                    'h_max': x1,
                    'mu': y0
                })
            else:
                regions.append({
                    'shape': 'triangle',
                    'h_min': x0,
                    'h_max': x1,
                    'mu0': y0,
                    'mu1': y1
                })
        return regions

    def _centroid_and_weight(self,
                             region: Dict[str, Any]
                             ) -> Tuple[float, float]:
        h_min = region['h_min']
        h_max = region['h_max']
        span = h_max - h_min

        if region['shape'] == 'rectangle':
            mu = region['mu']
            h_sr = h_min + span / 2
            w = mu * span

        else:  # triangle
            mu0 = region['mu0']
            mu1 = region['mu1']

            # sprawdzamy, czy trójkąt jest rosnący (mu1>mu0) czy malejący
            if mu1 > mu0:
                # rosnący fragment → centroida w 2/3 długości podstawy
                h_sr = h_min + 2 / 3 * span
            else:
                # malejący fragment → centroida w 1/3 długości podstawy
                h_sr = h_min + 1 / 3 * span

            delta_mu = abs(mu1 - mu0)
            # waga trójkąta: 1/2 * podstawa * wysokość różnicy mu
            w = 0.5 * delta_mu * span

        return h_sr, w

    def _interp(self,
                pts: List[List[float]],
                x: float
                ) -> float:
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if x0 <= x <= x1:
                if x1 == x0:
                    return max(y0, y1)
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return 0.0
