#!/usr/bin/env python3

import sys
from pathlib import Path
import subprocess
import json
from makeutils.colours import Colours, coloured_print
from makeutils.env import load_env, get_runner_paths
from makeutils.runners import run_process

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


def run_io_testcases(problem_type, problem_name, language, env_config, use_colours):
    runners = get_runner_paths(env_config)

    LANGUAGE_RUNNERS = {
        "cpp": {
            "ext": "cpp",
            "compile": lambda file: [
                runners["CPP_COMPILER"],
                "-std=c++17",
                "-O2",
                str(file),
                "-o",
                "temp.out",
            ],
            "run": lambda: ["./temp.out"],
        },
        "java": {
            "ext": "java",
            "compile": lambda file: [
                runners["JAVA_COMPILER"],
                "-d",
                "build",
                str(file),
            ],
            "run": lambda: [runners["JAVA_RUNNER"], "-cp", "build", problem_name],
        },
        "py": {
            "ext": "py",
            "compile": None,
            "run": lambda: [runners["PYTHON_RUNNER"], str(file_path)],
        },
        "js": {
            "ext": "js",
            "compile": None,
            "run": lambda: [runners["JS_RUNNER"], str(file_path)],
        },
    }

    lang = LANGUAGE_RUNNERS.get(language)
    if not lang:
        coloured_print(f"Unsupported language: {language}", Colours.RED)
        sys.exit(1)

    file_path = Path(problem_type) / language / f"{problem_name}.{lang['ext']}"
    test_file_path = Path("tests") / problem_type / f"{problem_name}.json"

    if not file_path.exists():
        coloured_print(f"Code file not found: {file_path}", Colours.RED)
        sys.exit(1)
    if not test_file_path.exists():
        coloured_print(f"Test file not found: {test_file_path}", Colours.RED)
        sys.exit(1)

    if lang["compile"]:
        compile_cmd = lang["compile"](file_path)
        success, _ = run_process(compile_cmd, use_colours=use_colours)
        if not success:
            coloured_print("Compilation failed.", Colours.RED)
            sys.exit(1)

    with open(test_file_path) as f:
        test_cases = json.load(f)

    passed = 0
    for i in range(len(test_cases)):
        test_case = test_cases[i]
        input_data = "\n".join(test_case["input"])
        expected_output = "\n".join(test_case["output"])

        run_cmd = lang["run"]()
        proc = subprocess.Popen(
            run_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        actual_output, _ = proc.communicate(input=input_data)

        actual_lines = [line.strip() for line in actual_output.strip().splitlines()]
        expected_lines = [line.strip() for line in expected_output.strip().splitlines()]

        if actual_lines == expected_lines:
            coloured_print(f"Test case {i} passed", Colours.GREEN, use_colours=use_colours)
            passed += 1
        else:
            coloured_print(f"Test case {i} failed", Colours.RED, use_colours=use_colours)
            for i, (exp, got) in enumerate(zip(expected_lines, actual_lines), 1):
                if exp != got:
                    print(f"  Line {i}:")
                    coloured_print(f"    Expected: {exp}", Colours.YELLOW, use_colours=use_colours)
                    coloured_print(f"    Got     : {got}", Colours.CYAN, use_colours=use_colours)
            if len(expected_lines) > len(actual_lines):
                for i in range(len(actual_lines), len(expected_lines)):
                    print(f"  Line {i+1}:")
                    coloured_print(f"    Expected: {expected_lines[i]}", Colours.YELLOW, use_colours=use_colours)
                    coloured_print(f"    Got     : <missing>", Colours.CYAN, use_colours=use_colours)
            elif len(actual_lines) > len(expected_lines):
                for i in range(len(expected_lines), len(actual_lines)):
                    print(f"  Line {i+1}:")
                    coloured_print(f"    Expected: <none>", Colours.YELLOW, use_colours=use_colours)
                    coloured_print(f"    Got     : {actual_lines[i]}", Colours.CYAN, use_colours=use_colours)


    print(f"\nResult: {passed}/{len(test_cases)} test cases passed.")

    if language == "cpp":
        Path("temp.out").unlink(missing_ok=True)

    if passed != len(test_cases):
        coloured_print(
            "Some test cases failed.", Colours.YELLOW, use_colours=use_colours
        )


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

run_io_testcases(problem_type, problem_name, language, env_config, USE_COLOURS)
