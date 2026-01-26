import random


class AbTesting:
    def __init__(self, ab_test_weights: dict[str, int]):
        self.ab_test_weights = ab_test_weights

        total_weight = sum(ab_test_weights.values())
        if total_weight == 0:
             raise ValueError("Total weight cannot be zero")

        self.thresholds = []
        cumulative_prob = 0.0

        for group, weight in ab_test_weights.items():
            probability = weight / total_weight
            cumulative_prob += probability
            self.thresholds.append((cumulative_prob, group))

    def get_group(self) -> str:
        rand = random.random()

        for threshold, group in self.thresholds:
            if rand < threshold:
                return group

        # Fallback for floating point rounding errors (e.g. rand=0.999999999999)
        return self.thresholds[-1][1]
