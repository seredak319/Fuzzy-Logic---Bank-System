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
            if alpha <= 0:
                continue

                # Jeżeli przynależność do funkcji jest zerowa to może pominąć - nie liczy się to do licznika ani mianownika
                # Np: mając
                # up_to_100k: 0.0
                # up_to_200k: 0.33
                # up_to_400k: 0.66
                # to pierwszą opcję możemy pominąć i przejść od razu do drugiej

            pts = self.output_mfs[decision][label]["points"]    # Bierzemy wykres dla danego label w postaci punktów np: [[100000,0], [200000,1], [300000,0]] (tu przykład dla up_to_200k)
            if pts[0][1] == 0 and pts[-1][1] == 0:              # Warunek sprawdzający niemonotoniczność funkcji - jeżeli pierwszy i ostatni punkt ma wartość 0 to jest niemonotoniczna (dla up_to_200k jest niemonotoniczna)
                cuts = self._cuts_for_alpha_cut(pts, alpha)     # Dla up_to_200k dla przynależności = 0.33 zwrócimy dwie wartości tj. 133k i 266k
                for z in cuts:                                  # I uwzględnimy obie w ważonej średniej gdzie alpha (0.33) to waga
                    num += alpha * z
                    den += alpha
            else:                                               # Dla punktów np [200000, 0] i [400000, 1] monotoniczna - rosnąca w tym przypadku
                z = self._invert_monotonic_mf(pts, alpha)
                num += alpha * z
                den += alpha
        return num / den if den else 0.0

    def _cuts_for_alpha_cut(self,
                            pts: List[List[float]],
                            alpha: float) -> List[float]:
        cuts: List[float] = []
        for (x0, mu0), (x1, mu1) in zip(pts, pts[1:]):
            if mu0 < mu1 and mu0 <= alpha <= mu1:
                cuts.append(x0 + (alpha - mu0) * (x1 - x0) / (mu1 - mu0))   # rosnące wzbocze
            if mu0 > mu1 and mu1 <= alpha <= mu0:
                cuts.append(x1 + (alpha - mu1) * (x0 - x1) / (mu0 - mu1))   # malejące wzbocze
            if mu0 == mu1 == alpha:
                cuts.extend([x0, x1])
        if not cuts:
            mus = [mu for _, mu in pts]
            if alpha >= max(mus):
                return [pts[mus.index(max(mus))][0]]
            return [pts[mus.index(min(mus))][0]]
        return cuts

    def _invert_monotonic_mf(self,
                             pts: List[List[float]],
                             alpha: float) -> float:
        for (x0, mu0), (x1, mu1) in zip(pts, pts[1:]):
            if mu0 == mu1 == alpha:
                return (x0 + x1) / 2
            if mu0 < mu1 and mu0 <= alpha <= mu1:
                return x0 + (alpha - mu0) * (x1 - x0) / (mu1 - mu0)     # rosnące wzbocze
            if mu0 > mu1 and mu1 <= alpha <= mu0:
                return x1 + (alpha - mu1) * (x0 - x1) / (mu0 - mu1)     # malejące wzbocze
        mus = [mu for _, mu in pts]
        if alpha >= max(mus):
            return pts[mus.index(max(mus))][0]
        return pts[mus.index(min(mus))][0]
