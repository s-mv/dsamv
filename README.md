# smv's DSA repository

That's it. Just me doing DSA.

Run solutions using **`python make.py <type> <problem> [lang]`**.

## Example usage:
```sh
python make.py arrays IsUnique          # runs arrays/cpp/IsUnique.cpp
python make.py arrays IsUnique java     # runs arrays/java/IsUnique.java
python make.py arrays Palindrome py     # runs arrays/python/Palindrome.py
python make.py list                     # shows all problems
python make.py list arrays              # shows only arrays problems
```

If there are any issues with `toml`, run `pip install toml` (Python < 3.11).

## Supported languages:
- **cpp** (default) - Compiles with g++ and runs
- **java** - Compiles with javac and runs
- **python, py** - Runs with python3
- **js** - Runs with node

## Configuration:
Create a `.env` file to customize compiler paths and enable colors:
```bash
COLOUR=True
CPP_COMPILER=g++
JAVA_COMPILER=javac
PYTHON_RUNNER=python3
JS_RUNNER=node
```

## Problem Lists:
Each problem type has its own description file:
- `arrays/DESC.md` - Array problems
- `graphs/DESC.md` - Graph problems  
- `DP/DESC.md` - Dynamic Programming problems
- `linkedlist/DESC.md` - Linked List problems

Or just run `python make.py list` to see what's implemented!

---

**PS:** This doesn't have advent of code solutions. If that's even considered
"DSA" really. :P It's fun though.
