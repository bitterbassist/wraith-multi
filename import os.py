import os

# Read the .env file and extract key-value pairs
def load_env(file_path='.env'):
    env_vars = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                env_vars[key] = value
    return env_vars

env_vars = load_env()
print(env_vars)  # Print out for reference
