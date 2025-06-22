# method/defuzzifier_type2.py

from typing import Dict, List, Any, Tuple


class Type2Defuzzifier:

    def __init__(self, output_mfs: Dict[str, Dict[str, Any]]):
        self.output_mfs = output_mfs

    def defuzzify(self,
                  degrees: Dict[str, float],
                  decision: str) -> float:

        # 1) Skalowanie
        #   np:
        #  z ->     [200000, 0], [300000, 1], [300000, 1], [300000, 1]
        #  na ->    [[200000, 0.0], [300000, 0.6666666666666666], [300000, 0.6666666666666666], [300000, 0.6666666666666666]]
        scaled = self._scale(degrees, decision)

        # 2) Suma przeskalowanych funkcji
        #   np:
        #  "up_to_200k": [[100000, 0.0], [200000, 0.33], [300000, 0.0]],
        #   "up_to_400k": [[200000, 0.0], [300000, 0.66], [300000, 0.66], [300000, 0.66]]
        #
        # Da rezultat -> [100000, 0], [200000, 0.33], [300000, 0.66], [300000, 0.66]
        aggregated = self._aggregate(scaled)

        # 3) Rozbijanie na regionty - Prostokąty i Trójkąty
        regions = self._decompose_to_P_and_T(aggregated)

        num, den = 0.0, 0.0
        for r in regions:
            h_sr, w = self._centroid_and_weight(r)
            num += h_sr * w
            den += w

        return num / den if den else 0.0

    def _scale(self,
               degrees: Dict[str, float],
               decision: str
               ) -> Dict[str, List[List[float]]]:
        out = {}
        for lbl, α in degrees.items():
            if α <= 0:
                continue
            pts = self.output_mfs[decision][lbl]['points']
            out[lbl] = [[x, μ * α] for x, μ in pts]
        return out

    def _aggregate(self,
                   scaled: Dict[str, List[List[float]]]
                   ) -> List[List[float]]:
        xs = sorted({x for pts in scaled.values() for x, _ in pts})
        agg = []
        for x in xs:
            μsum = sum(self._interp(pts, x) for pts in scaled.values())
            agg.append([x, μsum])
        return agg

    def _decompose_to_P_and_T(self,
                              agg: List[List[float]]
                              ) -> List[Dict[str, Any]]:
        regs = []
        for (x0, y0), (x1, y1) in zip(agg, agg[1:]):
            span = x1 - x0
            if abs(y0 - y1) < 1e-9:
                # czysty prostokąt
                regs.append({
                    'shape': 'P',
                    'h_min': x0, 'h_max': x1,
                    'μ': y0
                })
            else:
                # najpierw prostokąt o wysokości y_min
                y_min = min(y0, y1)
                regs.append({
                    'shape': 'P',
                    'h_min': x0, 'h_max': x1,
                    'μ': y_min
                })
                # resztę jako trójkąt o wysokości Δy = |y1–y0|
                Δy = abs(y1 - y0)
                if y1 > y0:
                    # rosnący trójkąt od 0→Δy
                    regs.append({
                        'shape': 'T',
                        'h_min': x0, 'h_max': x1,
                        'μ0': 0.0, 'μ1': Δy
                    })
                else:
                    # malejący trójkąt od Δy→0
                    regs.append({
                        'shape': 'T',
                        'h_min': x0, 'h_max': x1,
                        'μ0': Δy, 'μ1': 0.0
                    })
        return regs

    def _centroid_and_weight(self,
                             r: Dict[str, Any]
                             ) -> Tuple[float, float]:
        a, b = r['h_min'], r['h_max']
        span = b - a
        if r['shape'] == 'P':
            μ = r['μ']
            h_sr = a + span / 2
            w = μ * span
        else:
            μ0, μ1 = r['μ0'], r['μ1']
            w = 0.5 * abs(μ1 - μ0) * span
            #   centroid trójkąta: jeśli rośnie → 2/3, jeśli maleje → 1/3
            if μ1 > μ0:
                h_sr = a + 2 / 3 * span
            else:
                h_sr = a + 1 / 3 * span
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
