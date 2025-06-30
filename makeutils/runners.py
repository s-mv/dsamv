import subprocess
import os
import tempfile
from makeutils.colours import coloured_print, Colours
from pathlib import Path


def run_process(cmd, cwd=None, env=None, use_colours=True):
    """Run a command, capture output, print it, and return success and output."""
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=env)
    print(result.stdout, end="")
    if result.stderr:
        coloured_print(result.stderr, Colours.RED, end="", use_colours=use_colours)
    return result.returncode == 0, result.stdout


def generic_runner(
    compile_cmd=None,
    run_cmd=None,
    cwd=None,
    env=None,
    cleanup_files=None,
    use_colours=True,
):
    if compile_cmd:
        coloured_print(
            f"Compiling with: {' '.join(compile_cmd)}",
            Colours.CYAN,
            use_colours=use_colours,
        )
        success, _ = run_process(compile_cmd, cwd=cwd, env=env, use_colours=use_colours)
        if not success:
            coloured_print("Compilation failed", Colours.RED, use_colours=use_colours)
            return False, ""

    coloured_print(
        f"Running command: {' '.join(run_cmd)}", Colours.CYAN, use_colours=use_colours
    )
    success, output = run_process(run_cmd, cwd=cwd, env=env, use_colours=use_colours)

    if cleanup_files:
        for f in cleanup_files:
            try:
                os.unlink(f)
            except Exception:
                pass

    return success, output


def run_cpp(file_path, runners, test_file_path=None, use_colours=True):
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)

    exe_path = build_dir / "temp"

    compile_cmd = [
        runners["CPP_COMPILER"],
        "-std=c++17",
        "-O2",
        str(file_path),
        "helpers/JSON.cpp",
        "-I",
        "./helpers",
        "-o",
        str(exe_path),
    ]

    run_cmd = [str(exe_path)]

    if test_file_path and os.path.exists(test_file_path):
        run_cmd.append(str(test_file_path))

    success, output = generic_runner(
        compile_cmd=compile_cmd,
        run_cmd=run_cmd,
        cleanup_files=[exe_path],
        use_colours=use_colours,
    )
    return success, output


def run_java(file_path, runners, test_file_path=None, use_colours=True):
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)

    problem_type = file_path.parent.parent.name
    class_name = file_path.stem

    compile_cmd = [
        runners["JAVA_COMPILER"],
        "-d",
        "build",
        "helpers/*.java",
        str(file_path),
    ]

    fq_class_name = f"{problem_type}.java.{class_name}"

    run_cmd = [runners["JAVA_RUNNER"], "-cp", "build", fq_class_name]

    if test_file_path and os.path.exists(test_file_path):
        run_cmd.append(str(test_file_path))

    manual_cmd = (
        f"javac -d build helpers/*.java {file_path} && java -cp build {fq_class_name}"
    )
    if test_file_path and os.path.exists(test_file_path):
        manual_cmd += f" {test_file_path}"
    coloured_print(
        f"Equivalent command: {manual_cmd}", Colours.CYAN, use_colours=use_colours
    )

    return generic_runner(
        compile_cmd=compile_cmd, run_cmd=run_cmd, use_colours=use_colours
    )


def run_python(file_path, runners, test_file_path=None, use_colours=True):
    env = os.environ.copy()
    env["PYTHONPATH"] = f"helpers:{env.get('PYTHONPATH', '')}"

    python_cmd = f"PYTHONPATH=helpers {runners['PYTHON_RUNNER']} {file_path}"
    if test_file_path and os.path.exists(test_file_path):
        python_cmd += f" {test_file_path}"
    coloured_print(
        f"Equivalent command: {python_cmd}", Colours.CYAN, use_colours=use_colours
    )

    run_cmd = [runners["PYTHON_RUNNER"], str(file_path)]

    if test_file_path and os.path.exists(test_file_path):
        run_cmd.append(str(test_file_path))

    return generic_runner(run_cmd=run_cmd, env=env, use_colours=use_colours)


def run_javascript(file_path, runners, test_file_path=None, use_colours=True):
    run_cmd = [runners["JS_RUNNER"], str(file_path)]

    if test_file_path and os.path.exists(test_file_path):
        run_cmd.append(str(test_file_path))

    return generic_runner(run_cmd=run_cmd, use_colours=use_colours)
