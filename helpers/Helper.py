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

        for input_str, expected in tests.items():
            result = solution_instance.solution(input_str)
            ok = result == expected
            print(f"'{input_str}' => {'PASSED' if ok else f'FAILED (got {result})'}")
            if ok:
                passed += 1
            total += 1

        print(f"\n{passed}/{total} tests passed.")
