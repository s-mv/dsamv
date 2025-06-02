from pathlib import Path

def load_env():
    env_config = {}
    env_file = Path('.env')
    if env_file.exists():
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_config[key.strip()] = value.strip().strip('"\'')
        except Exception as e:
            print(f"Warning: Could not read .env file: {e}")
    return env_config

def get_runner_paths(env_config):
    defaults = {
        'CPP_COMPILER': 'g++',
        'JAVA_COMPILER': 'javac',
        'JAVA_RUNNER': 'java',
        'PYTHON_RUNNER': 'python3',
        'JS_RUNNER': 'node'
    }
    return {key: env_config.get(key, default) for key, default in defaults.items()}
