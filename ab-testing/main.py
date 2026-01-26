from ab_testing import AbTesting

AB_TEST_WEIGHTS = {
    "A": 2,
    "B": 7,
    "C": 1,
}

def main():
    ab_testing = AbTesting(AB_TEST_WEIGHTS)
    for num in range(0, 20):
        print(f"A/B test group: {ab_testing.get_group()}")


if __name__ == "__main__":
    main()
