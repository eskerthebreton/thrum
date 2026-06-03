import yaml
from pathlib import Path

def read_yaml(path):
    with open(path, 'r') as fp:
        try:
            result = yaml.safe_load(fp)
        except yaml.YAMLError as e:
            print(e)
    return result

def read_string(path):
    with open(path, 'r') as fp:
        result = fp.read()
    return result
        

def write_md(string, path):
    with open(path, 'w') as file:
        file.write(string)

def read_ability(name, ability_type):
    print(f"- Reading ability '{name}'")
    file = Path("../abilities") / ability_type / f"{name}.yml"
    result = read_yaml(file)
    return result
