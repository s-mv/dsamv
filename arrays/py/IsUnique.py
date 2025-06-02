class IsUnique:
    def __init__(self):
        self.tests = {
            "you shall not pass": False,
            "you can": True,
            "you cannot": False,
            "maybe no?": True
        }

    @staticmethod
    def solution(input_str):
        seen = []
        for char in input_str:
            if char in seen:
                return False
            seen.append(char)
        return True

    def run_tests(self):
        for input_str, expected in self.tests.items():
            result = self.solution(input_str)
            print(f"Running input '{input_str}' -> {'PASSED' if result == expected else 'FAILED'}")

tester = IsUnique()
tester.run_tests()
