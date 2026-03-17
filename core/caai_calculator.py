import numpy as np

class CAAICalculator:
    def compute_individual_score(self, participant):
        return 0.6

    def compute_group_caai(self, participants):
        if not participants:
            return 0.5
        return float(np.mean([p.alignment_score for p in participants]))

    def _compute_synchrony(self, participants):
        return 0.7
