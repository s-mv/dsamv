#!/usr/bin/env python3

import sys
import os
from pathlib import Path
import subprocess
import json

from makeutils.colours import Colours, coloured_print
from makeutils.env import load_env, get_runner_paths
from makeutils.runners import run_cpp, run_java, run_javascript, run_python

env_config = load_env()
USE_COLOURS = env_config.get("COLOUR", "False").lower() == "true"


def get_file_path(problem_type, problem_name, language):
    extensions = {
        "cpp": "cpp",
        "java": "java",
        "python": "py",
        "py": "py",
        "js": "js",
        "javascript": "js",
    }

    if language not in extensions:
        return None

    ext = extensions[language]
    return Path(problem_type) / ext / f"{problem_name}.{ext}"


def get_test_file_path(problem_type, problem_name):
    """Get the path to the test file for a problem."""
    return Path("tests") / problem_type / f"{problem_name}.json"


def list_problems(problem_type=None):
    base_folders = ["arrays", "graphs", "DP", "linkedlist", "codeforces"]
    languages = ["cpp", "java", "py", "js"]
    extensions = {"cpp": "cpp", "java": "java", "py": "py", "js": "js"}

    if problem_type:
        if problem_type in base_folders:
            base_folders = [problem_type]
        else:
            coloured_print(f"Unknown problem type: {problem_type}", Colours.RED)
            coloured_print(
                f"Available types: {', '.join(base_folders)}", Colours.YELLOW
            )
            return

    for topic in base_folders:
        test_dir = Path("tests") / topic
        if not test_dir.exists():
            continue

        coloured_print(f"\n{topic.lower()}:", Colours.BOLD)

        problems = {}

        for json_file in test_dir.glob("*.json"):
            problem_name = json_file.stem
            problems[problem_name] = []

        for problem in problems:
            for lang in languages:
                code_file = Path(topic) / lang / f"{problem}.{extensions[lang]}"
                if code_file.exists():
                    problems[problem].append(lang)

        for problem, langs in sorted(problems.items()):
            if langs:
                lang_str = ", ".join(sorted(langs))
                coloured_print(f"  {problem}", Colours.GREEN, end="")
                print(f" ({lang_str})")
            else:
                coloured_print(f"  {problem} (test cases only)", Colours.YELLOW)


if len(sys.argv) < 2:
    coloured_print("Usage: python dsa.py <type> <problem> [lang]", Colours.BOLD)
    coloured_print("       python dsa.py list [type]", Colours.BOLD)
    print("\nExamples:")
    coloured_print(
        "  python dsa.py arrays IsUnique          # runs arrays/cpp/IsUnique.cpp",
        Colours.GREEN,
    )
    coloured_print(
        "  python dsa.py arrays IsUnique java     # runs arrays/java/IsUnique.java",
        Colours.GREEN,
    )
    coloured_print(
        "  python dsa.py lists LinkedList py      # runs lists/python/LinkedList.py",
        Colours.GREEN,
    )
    coloured_print(
        "  python dsa.py list                     # shows all problems", Colours.GREEN
    )
    coloured_print(
        "  python dsa.py list arrays              # shows only arrays problems",
        Colours.GREEN,
    )
    print("\nSupported languages:")
    print("  cpp (default) - Compiles with g++ and runs")
    print("  java         - Compiles with javac and runs")
    print("  python, py   - Runs with python3")
    print("  js           - Runs with node")
    sys.exit(1)


def run_codeforces(problem_name, language, env_config, use_colours):
    file_path = Path("codeforces") / f"{problem_name}.{language}"
    test_file_path = Path("tests") / "cf" / f"{problem_name}.json"

    if not file_path.exists():
        coloured_print(
            f"Error: {file_path} does not exist.", Colours.RED, use_colours=use_colours
        )
        sys.exit(1)

    if not test_file_path.exists():
        coloured_print(
            f"Error: Test file {test_file_path} does not exist.",
            Colours.RED,
            use_colours=use_colours,
        )
        sys.exit(1)

    # Read test cases from JSON
    with open(test_file_path, "r") as f:
        test_cases = json.load(f)

    # Prepare the command to run the solution
    runners = get_runner_paths(env_config)
    language_runners = {
        "cpp": [
            runners["CPP_COMPILER"],
            "-std=c++17",
            "-O2",
            str(file_path),
            "-o",
            "temp.out",
        ],
        "java": [runners["JAVA_COMPILER"], "-d", "build", str(file_path)],
        "py": [runners["PYTHON_RUNNER"], str(file_path)],
        "js": [runners["JS_RUNNER"], str(file_path)],
    }

    if language not in language_runners:
        coloured_print(
            f"Unsupported language: {language}", Colours.RED, use_colours=use_colours
        )
        sys.exit(1)

    # Compile if necessary
    if language in ["cpp", "java"]:
        compile_cmd = language_runners[language]
        success, _ = run_process(compile_cmd, use_colours=use_colours)
        if not success:
            coloured_print("Compilation failed.", Colours.RED, use_colours=use_colours)
            sys.exit(1)

    # Run tests
    passed = 0
    for test_case in test_cases:
        input_data = "\n".join(test_case["input"])
        expected_output = "\n".join(test_case["output"])

        if language == "cpp":
            run_cmd = ["./temp.out"]
        elif language == "java":
            run_cmd = [runners["JAVA_RUNNER"], "-cp", "build", problem_name]
        elif language == "py":
            run_cmd = [runners["PYTHON_RUNNER"], str(file_path)]
        elif language == "js":
            run_cmd = [runners["JS_RUNNER"], str(file_path)]

        process = subprocess.Popen(
            run_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
        )
        actual_output, _ = process.communicate(input=input_data)

        if actual_output.strip() == expected_output.strip():
            coloured_print(
                f"Test case passed: Input: {input_data}",
                Colours.GREEN,
                use_colours=use_colours,
            )
            passed += 1
        else:
            coloured_print(
                f"Test case failed: Input: {input_data}",
                Colours.RED,
                use_colours=use_colours,
            )
            print(f"Expected: {expected_output}")
            print(f"Got: {actual_output}")

    print(f"\n{passed}/{len(test_cases)} test cases passed.")

    # Cleanup
    if language == "cpp":
        Path("temp.out").unlink()


if sys.argv[1] == "clean":
    build_dir = Path("build")
    if build_dir.exists() and build_dir.is_dir():
        import shutil

        shutil.rmtree(build_dir)
        coloured_print("Build directory cleaned.", Colours.GREEN)
    else:
        coloured_print("No build directory to clean.", Colours.YELLOW)
    sys.exit(0)


if sys.argv[1] == "list":
    list_type = sys.argv[2] if len(sys.argv) > 2 else None
    list_problems(list_type)
    sys.exit(0)

problem_type = sys.argv[1]
problem_name = sys.argv[2]
language = sys.argv[3] if len(sys.argv) > 3 else "cpp"

file_path = get_file_path(problem_type, problem_name, language)

if not file_path:
    coloured_print(f"Unsupported language: {language}", Colours.RED)
    print("Supported languages: cpp, java, python, py, js")
    sys.exit(1)

if not file_path.exists():
    coloured_print(
        f"Oh sorry, {file_path} might still not exist - you can always contribute to the repository!",
        Colours.YELLOW,
    )
    sys.exit(1)

test_file_path = get_test_file_path(problem_type, problem_name)

if not test_file_path.exists():
    coloured_print(
        f"Warning: Test file {test_file_path} not found. Running without tests.",
        Colours.YELLOW,
    )

if problem_type in ["cf", "codeforces"]:
    run_codeforces(problem_name, language, env_config, USE_COLOURS)
    sys.exit(0)


language_runners = {
    "cpp": run_cpp,
    "java": run_java,
    "python": run_python,
    "py": run_python,
    "js": run_javascript,
    "javascript": run_javascript,
}

runners = get_runner_paths(env_config)

runner_func = language_runners[language]
success, output = runner_func(
    file_path, runners, test_file_path=test_file_path, use_colours=USE_COLOURS
)

if not success:
    sys.exit(1)
