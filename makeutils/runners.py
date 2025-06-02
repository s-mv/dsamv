import subprocess
import os
import tempfile
from makeutils.colours import coloured_print, Colours

def run_process(cmd, cwd=None, use_colours=True):
    """Run a command, capture output, print it, and return success and output."""
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    print(result.stdout, end='')
    if result.stderr:
        coloured_print(result.stderr, Colours.RED, end='', use_colours=use_colours)
    return result.returncode == 0, result.stdout

def generic_runner(
    compile_cmd=None,       # list of strings or None
    run_cmd=None,           # list of strings
    cwd=None,
    cleanup_files=None,     # list of Path or str to delete after run
    use_colours=True
):
    if compile_cmd:
        coloured_print(f"Compiling with: {' '.join(compile_cmd)}", Colours.CYAN, use_colours=use_colours)
        success, _ = run_process(compile_cmd, cwd=cwd, use_colours=use_colours)
        if not success:
            coloured_print("Compilation failed", Colours.RED, use_colours=use_colours)
            return False, ""

    coloured_print(f"Running command: {' '.join(run_cmd)}", Colours.CYAN, use_colours=use_colours)
    success, output = run_process(run_cmd, cwd=cwd, use_colours=use_colours)

    if cleanup_files:
        for f in cleanup_files:
            try:
                os.unlink(f)
            except Exception:
                pass

    return success, output

def run_cpp(file_path, runners, use_colours=True):
    with tempfile.NamedTemporaryFile(suffix='.exe', delete=False) as tmp:
        exe_path = tmp.name

    compile_cmd = [runners['CPP_COMPILER'], '-std=c++17', '-O2', str(file_path), '-o', exe_path]
    run_cmd = [exe_path]

    success, output = generic_runner(
        compile_cmd=compile_cmd,
        run_cmd=run_cmd,
        cleanup_files=[exe_path],
        use_colours=use_colours
    )
    return success, output

def run_java(file_path, runners, use_colours=True):
    java_dir = file_path.parent
    class_name = file_path.stem

    compile_cmd = [runners['JAVA_COMPILER'], file_path.name]
    run_cmd = [runners['JAVA_RUNNER'], class_name]
    cleanup_files = [java_dir / f"{class_name}.class"]

    return generic_runner(
        compile_cmd=compile_cmd,
        run_cmd=run_cmd,
        cwd=java_dir,
        cleanup_files=cleanup_files,
        use_colours=use_colours
    )

def run_python(file_path, runners, use_colours=True):
    run_cmd = [runners['PYTHON_RUNNER'], str(file_path)]
    return generic_runner(run_cmd=run_cmd, use_colours=use_colours)

def run_javascript(file_path, runners, use_colours=True):
    run_cmd = [runners['JS_RUNNER'], str(file_path)]
    return generic_runner(run_cmd=run_cmd, use_colours=use_colours)
