#!/usr/bin/env python3

import sys
import os
import subprocess
import tempfile
from pathlib import Path

from makeutils.colours import Colours, coloured_print
from makeutils.env import load_env, get_runner_paths
from makeutils.runners import run_cpp, run_java, run_javascript, run_python

try:
    import tomllib
    def load_toml(file_path):
        with open(file_path, 'rb') as f:
            return tomllib.load(f)
except:
    import toml
    def load_toml(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return toml.load(f)

env_config = load_env()
USE_COLOURS = env_config.get('COLOUR', 'False').lower() == 'true'

def get_file_path(problem_type, problem_name, language):
    extensions = {
        'cpp': 'cpp',
        'java': 'java', 
        'python': 'py',
        'py': 'py',
        'js': 'js',
        'javascript': 'js'
    }
    
    if language not in extensions:
        return None

    ext = extensions[language]
    return Path(problem_type) / ext / f"{problem_name}.{ext}"

def list_problems(problem_type=None):
    folders_to_check = ['arrays', 'graphs', 'DP', 'linkedlist']
    
    if problem_type:
        if problem_type in folders_to_check:
            folders_to_check = [problem_type]
        else:
            coloured_print(f"Unknown problem type: {problem_type}", Colours.RED)
            coloured_print(f"Available types: {', '.join(folders_to_check)}", Colours.YELLOW)
            return
    
    languages = ['cpp', 'java', 'python', 'js']
    extensions = {'cpp': 'cpp', 'java': 'java', 'python': 'py', 'js': 'js'}
    
    for folder in folders_to_check:
        folder_path = Path(folder)
        if not folder_path.exists():
            continue
            
        coloured_print(f"\n{folder.lower()}:", Colours.BOLD)
        
        problems = {}
        
        for lang in languages:
            lang_dir = folder_path / lang
            if lang_dir.exists():
                for file_path in lang_dir.glob(f"*.{extensions[lang]}"):
                    problem_name = file_path.stem
                    if problem_name not in problems:
                        problems[problem_name] = []
                    problems[problem_name].append(lang)
        
        if not problems:
            coloured_print("  No problems found", Colours.YELLOW)
        else:
            for problem, langs in sorted(problems.items()):
                lang_str = ', '.join(sorted(langs))
                coloured_print(f"  {problem}", Colours.GREEN, end='')
                print(f" ({lang_str})")

if len(sys.argv) < 2:
    coloured_print("Usage: python make.py <type> <problem> [lang]", Colours.BOLD)
    coloured_print("       python make.py list [type]", Colours.BOLD)
    print("\nExamples:")
    coloured_print("  python make.py arrays IsUnique          # runs arrays/cpp/IsUnique.cpp", Colours.GREEN)
    coloured_print("  python make.py arrays IsUnique java     # runs arrays/java/IsUnique.java", Colours.GREEN) 
    coloured_print("  python make.py lists LinkedList py      # runs lists/python/LinkedList.py", Colours.GREEN)
    coloured_print("  python make.py list                     # shows all problems", Colours.GREEN)
    coloured_print("  python make.py list arrays              # shows only arrays problems", Colours.GREEN)
    print("\nSupported languages:")
    print("  cpp (default) - Compiles with g++ and runs")
    print("  java         - Compiles with javac and runs")
    print("  python, py   - Runs with python3")
    print("  js           - Runs with node")
    sys.exit(1)

if sys.argv[1] == 'list':
    list_type = sys.argv[2] if len(sys.argv) > 2 else None
    list_problems(list_type)
    sys.exit(0)

problem_type = sys.argv[1]
problem_name = sys.argv[2]
language = sys.argv[3] if len(sys.argv) > 3 else 'cpp'

file_path = get_file_path(problem_type, problem_name, language)

if not file_path:
    coloured_print(f"Unsupported language: {language}", Colours.RED)
    print("Supported languages: cpp, java, python, py, js")
    sys.exit(1)

if not file_path.exists():
    coloured_print(f"Oh sorry, {file_path} might still not exist - you can always contribute to the repository!", Colours.YELLOW)
    sys.exit(1)

language_runners = {
    'cpp': run_cpp,
    'java': run_java,
    'python': run_python,
    'py': run_python,
    'js': run_javascript,
    'javascript': run_javascript
}

runners = get_runner_paths(env_config)

runner_func = language_runners[language]
success = runner_func(file_path, runners)

if not success:
    sys.exit(1)
