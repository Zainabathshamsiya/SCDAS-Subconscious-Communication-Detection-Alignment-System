import numpy as np

class MicroExpression:

    def detect(self, prev_frame, current_frame):

        diff = np.mean(abs(current_frame - prev_frame))

        if diff > 15:
            return "micro_expression_detected"

        return "stable"
