import random

class AbTestingRangeError(Exception):
    pass


class AbTesting:
    def __init__(self, ab_test_weights: dict[str, int]):
        self.ab_test_weights = ab_test_weights

        self.ab_test_weights_pairs = self.ab_test_weights.items()

        self.weights_sum = 0.0
        for group, weight in self.ab_test_weights_pairs:
            self.weights_sum += weight

        self.prob_offsets_dict = {}

    def get_group(self) -> str:
        rand = random.random()
        # print(f"Random: {rand}")

        prob_offset = 0.0
        for group, weight in self.ab_test_weights_pairs:
            if group in self.prob_offsets_dict:
                offset = self.prob_offsets_dict[group]
            else:
                offset = weight / self.weights_sum
                self.prob_offsets_dict[group] = offset

            # print(f"Range: {prob_offset} - {prob_offset + offset} for group {group}")
            if rand >= prob_offset and rand <= prob_offset + offset:
                return group

            prob_offset += offset

        raise AbTestingRangeError("Random doesn't fall into any of groups!")
