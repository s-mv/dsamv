# smv's DSA repository

Do your DSA in the CLI, because that's what crazy people do.

Might repurpose this for something crazier like DSA in particular assembly
flavours. I might survive this experience somehow and live to see it work.

~~PS: I just wrote my own JSON parsers for testing... Isn't the proof enough~~
~~that I must be good at DSA?~~

**Pull requests are welcome for automating testing further (using legitimate APIs**
**to fetch tests and such things).**

Run solutions using **`python dsa.py <type> <problem> [lang]`**.

## Example usage:
```sh
python dsa.py arrays IsUnique          # runs arrays/cpp/IsUnique.cpp
python dsa.py arrays IsUnique java     # runs arrays/java/IsUnique.java
python dsa.py arrays Palindrome py     # runs arrays/python/Palindrome.py
python dsa.py list                     # shows all problems
python dsa.py list arrays              # shows only arrays problems

python dsa.py clean                    # cleans up build cache
```

### Run Codeforces problems:
Example:
```sh
python dsa.py cf P4A
python dsa.py codeforces P71A cpp
```

## Supported languages:
- **cpp** (default) - Compiles with g++ and runs
- **java** - Compiles with javac and runs
- **python, py** - Runs with python3
- **js** - Runs with node

## Configuration:
You may modify the `.env` file to customize compiler paths and enable colors:
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

Or just run `python dsa.py list` to see what's implemented!


## Write your own
Refer to [./templates/](./templates/) for templates to add  your own test cases
and problems.

- [CodeForces.json](./templates/CodeForces.json) JSON template for Codeforces-style problems
- [Template.json](./templates/Template.json): Basic input-output test case format
- [Template.cpp](./templates/Template.cpp): C++ starter template for problems
- [Template.py](./templates/Template.py): Python starter template
- [Template.java](./templates/Template.java): Java starter template
- [Template.js](./templates/Template.js): JavaScript starter template

---

**PS:** This doesn't have advent of code solutions. If that's even considered
"DSA" really. :P It's fun though.
