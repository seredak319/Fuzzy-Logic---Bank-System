# method/defuzzifier.py

"""
Defuzyfikacja typu 1 (Mamdani, metoda „odwrotnego mapowania”)

Po wnioskowaniu mamy dla każdej wyjściowej etykiety „label” poziom aktywacji α ∈ [0,1].
Zgodnie z podręcznikowym schematem:
  1. Wyjściowe funkcje przynależności MUSZĄ być monotoniczne (rosnące lub malejące),
     żeby istniało jednoznaczne odwzorowanie odwrotne μ⁻¹(α)=z.
     – Jeśli któraś etykieta ma kształt „górki” (np. trapez lub pełny trójkąt),
       należy ją wcześniej podzielić na dwie monotoniczne (np. mid_low i mid_high).
  2. Dla każdej etykiety obliczamy z_i = μ_label⁻¹(α) – punkt, w którym funkcja
     przyjmuje wartość α.
  3. Ostateczny wynik:
        z* = (Σ α · z_i) / (Σ α)

Poniższa klasa _odwzorowuje MF i liczy z* dokładnie wg tej metody.
"""

from typing import Dict, List, Any

class Type1Defuzzifier:
    def __init__(self, output_mfs: Dict[str, Dict[str, Any]]):
        self.output_mfs = output_mfs

    def defuzzify(self,
                  degrees: Dict[str, float],
                  decision: str) -> float:
        num = 0.0
        den = 0.0
        for label, alpha in degrees.items():
            pts = self.output_mfs[decision][label]["points"]
            z = self._invert_monotonic_mf(pts, alpha)
            num += alpha * z
            den += alpha
        return num/den if den else 0.0

    def _invert_monotonic_mf(self,
                             pts: List[List[float]],
                             alpha: float) -> float:
        # pts = [[x0,μ0], [x1,μ1], ..., [xn,μn]]
        # znajdź odcinek, na którym μ przechodzi przez α
        for (x0,μ0), (x1,μ1) in zip(pts, pts[1:]):
            if μ0 == μ1 == alpha:
                # płaski odcinek dokładnie na poziomie α
                return (x0 + x1)/2
            if μ0 < μ1 and μ0 <= alpha <= μ1:
                # monotonicznie rosnący fragment
                return x0 + (alpha - μ0)*(x1 - x0)/(μ1 - μ0)
            if μ0 > μ1 and μ1 <= alpha <= μ0:
                # monotonicznie malejący fragment
                return x1 + (alpha - μ1)*(x0 - x1)/(μ0 - μ1)
        # jeśli α leży poza zakresem [min(μ), max(μ)], zwróć skrajny punkt
        μs = [μ for _,μ in pts]
        if alpha >= max(μs):
            # najwyższa wiarygodność → x przy μ_max
            return pts[μs.index(max(μs))][0]
        # najniższa wiarygodność
        return pts[μs.index(min(μs))][0]
