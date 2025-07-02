import json
import sys
import os


class Helper:
    @staticmethod
    def test(solution_instance):
        if len(sys.argv) < 2:
            print("Usage: python your_script.py <test_file.json>")
            sys.exit(1)

        test_file = sys.argv[1]
        if not os.path.exists(test_file):
            print(f"Test file not found: {test_file}")
            sys.exit(1)

        with open(test_file, "r") as f:
            tests = json.load(f)

        passed = 0
        total = 0

        for test_case in tests:
            input_args = test_case["input"]
            expected = test_case["expected"]

            if not isinstance(input_args, list):
                print(f"Error: 'input' must be a list. Got: {type(input_args)}")
                sys.exit(1)

            try:
                result = solution_instance.solution(*input_args)
                ok = result == expected
                print(
                    f"Input: {input_args} => {'PASSED' if ok else f'FAILED (got {result}, expected {expected})'}"
                )
                if ok:
                    passed += 1
            except Exception as e:
                print(f"Error while testing input {input_args}: {e}")

            total += 1

        print(f"\n{passed}/{total} tests passed.")
