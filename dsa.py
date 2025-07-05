#!/usr/bin/env python3

import sys
import os
from pathlib import Path
import subprocess
import json

from makeutils.colours import Colours, coloured_print
from makeutils.env import load_env, get_runner_paths
from makeutils.runners import run_cpp, run_java, run_javascript, run_process, run_python

env_config = load_env()
USE_COLOURS = env_config.get("COLOUR", "False").lower() == "true"

PROBLEM_TYPE_ALIASES = {
    "cf": "codeforces",
    "linkedlists": "linkedlist",
    "graph": "graphs",
    "dp": "DP",
}

LANGUAGE_ALIASES = {
    "c++": "cpp",
    "cpp": "cpp",
    "python": "py",
    "py": "py",
    "js": "js",
    "javascript": "js",
    "node": "js",
    "java": "java",
    "javac": "java",
}


def get_file_path(problem_type, problem_name, language_folder):
    ext = language_folder
    return Path(problem_type) / ext / f"{problem_name}.{ext}"


def get_test_file_path(problem_type, problem_name):
    return Path("tests") / problem_type / f"{problem_name}.json"


def list_problems(problem_type=None):
    base_folders = ["arrays", "graphs", "DP", "linkedlist", "codeforces"]
    languages = ["cpp", "java", "py", "js"]
    extensions = {"cpp": "cpp", "java": "java", "py": "py", "js": "js"}

    if problem_type:
        if problem_type in base_folders:
            base_folders = [problem_type]
        else:
            coloured_print(f"Unknown problem category: {problem_type}", Colours.RED)
            coloured_print(
                f"Available categories: {', '.join(base_folders)}", Colours.YELLOW
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
    coloured_print("  python dsa.py arrays IsUnique", Colours.GREEN)
    coloured_print("  python dsa.py arrays IsUnique java", Colours.GREEN)
    coloured_print("  python dsa.py linkedlist LinkedList py", Colours.GREEN)
    coloured_print("  python dsa.py list", Colours.GREEN)
    coloured_print("  python dsa.py list arrays", Colours.GREEN)
    print("\nSupported languages:")
    print("  cpp (default), java, python, javascript")
    print("\nLanguage aliases:")
    print(
        "  py -> python, js -> javascript, c++ -> cpp, node -> javascript, javac -> java"
    )
    print("Problem type aliases:")
    print("  cf -> codeforces, graph -> graphs, dp -> DP, linkedlists -> linkedlist")
    sys.exit(1)


def run_codeforces(problem_name, language, env_config, use_colours):
    file_path = Path("codeforces") / language / f"{problem_name}.{language}"
    test_file_path = Path("tests") / "codeforces" / f"{problem_name}.json"

    if not file_path.exists():
        coloured_print(
            f"Error: Code file not found: {file_path}",
            Colours.RED,
            use_colours=use_colours,
        )
        sys.exit(1)

    if not test_file_path.exists():
        coloured_print(
            f"Error: Test file not found: {test_file_path}",
            Colours.RED,
            use_colours=use_colours,
        )
        sys.exit(1)

    with open(test_file_path, "r") as f:
        test_cases = json.load(f)

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
            f"Error: Unsupported language '{language}'",
            Colours.RED,
            use_colours=use_colours,
        )
        sys.exit(1)

    if language in ["cpp", "java"]:
        compile_cmd = language_runners[language]
        success, _ = run_process(compile_cmd, use_colours=use_colours)
        if not success:
            coloured_print(
                "Compilation failed. Please check your code for errors.",
                Colours.RED,
                use_colours=use_colours,
            )
            sys.exit(1)

    passed = 0
    for test_case in test_cases:
        input_data = "\n".join(test_case["input"])
        expected_output = "\n".join(test_case["output"])

        if language == "cpp":
            run_cmd = ["./temp.out"]
        elif language == "java":
            run_cmd = [runners["JAVA_RUNNER"], "-cp", "build", problem_name]
        else:
            run_cmd = language_runners[language]

        process = subprocess.Popen(
            run_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
        )
        actual_output, _ = process.communicate(input=input_data)

        if actual_output.strip() == expected_output.strip():
            coloured_print("Test case passed", Colours.GREEN, use_colours=use_colours)
            passed = passed + 1
            print(f"Input:\n{input_data}\n")
        else:
            coloured_print("Test case failed", Colours.RED, use_colours=use_colours)
            print(f"Input:\n{input_data}")
            print(f"Expected:\n{expected_output}")
            print(f"Got:\n{actual_output.strip()}\n")

    print(f"\nResult: {passed}/{len(test_cases)} test cases passed.")
    if passed != len(test_cases):
        coloured_print(
            "Some test cases failed. Please review the output above.",
            Colours.YELLOW,
            use_colours=use_colours,
        )

    if language == "cpp":
        Path("temp.out").unlink()


if sys.argv[1] == "clean":
    build_dir = Path("build")
    if build_dir.exists() and build_dir.is_dir():
        import shutil

        shutil.rmtree(build_dir)
        coloured_print("Build directory cleaned.", Colours.GREEN)
    else:
        coloured_print("No build directory found to clean.", Colours.YELLOW)
    sys.exit(0)


if sys.argv[1] == "list":
    list_type = sys.argv[2] if len(sys.argv) > 2 else None
    list_type = PROBLEM_TYPE_ALIASES.get(list_type, list_type) if list_type else None
    list_problems(list_type)
    sys.exit(0)

problem_name = sys.argv[2]
problem_type_input = sys.argv[1]
language_input = sys.argv[3] if len(sys.argv) > 3 else "cpp"

problem_type = PROBLEM_TYPE_ALIASES.get(
    problem_type_input.lower(), problem_type_input.lower()
)
language = LANGUAGE_ALIASES.get(language_input.lower(), language_input.lower())

file_path = get_file_path(problem_type, problem_name, language)

if not file_path:
    coloured_print(f"Error: Unsupported language '{language}'", Colours.RED)
    print("Supported languages: cpp, java, python, javascript")
    print(
        "Aliases: cf -> codeforces, graph -> graphs, linkedlists -> linkedlist, dp -> DP"
    )
    sys.exit(1)

if not file_path.exists():
    coloured_print(f"Code file not found: {file_path}", Colours.YELLOW)
    print("Tip: Make sure the file exists or consider contributing a solution.")
    sys.exit(1)

test_file_path = get_test_file_path(problem_type, problem_name)

if not test_file_path.exists():
    coloured_print(f"Test file not found: {test_file_path}", Colours.YELLOW)
    print("This problem will run without correctness tests.")

if problem_type == "codeforces":
    run_codeforces(problem_name, language, env_config, USE_COLOURS)
    sys.exit(0)


language_runners = {
    "cpp": run_cpp,
    "java": run_java,
    "py": run_python,
    "js": run_javascript,
}

runners = get_runner_paths(env_config)

runner_func = language_runners.get(language)
if not runner_func:
    coloured_print(f"Error: Unsupported language runner for '{language}'", Colours.RED)
    sys.exit(1)

success, output = runner_func(
    file_path, runners, test_file_path=test_file_path, use_colours=USE_COLOURS
)

if not success:
    sys.exit(1)
