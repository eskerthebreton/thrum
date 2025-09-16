import yaml
import pandas as pd
from pathlib import Path

def read_yaml(path):
    with open(path, 'r') as file:
        try:
            result = yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(e)
    return result
         
def read_ability(name, ability_type):
    file = Path("../abilities") / ability_type / f"{name}.yml"
    result = read_yaml(file)
    return result

def format_ability_string(ability_dict):
    name = ability_dict["name"]
    category = ability_dict["type"]
    tags_text = ", ".join(ability_dict["tags"])
    parenthetical = f" ({tags_text})" if tags_text else ""
    header_md = f"## {name}"
    type_md = f"**Type:** {category}{parenthetical}"
    parameters_md = "\n".join([f"**{k}**: {v}" for k,v in ability_dict["parameters"].items()])
    parameters_plain = "\n".join([f"{k}: {v}" for k,v in ability_dict["parameters"].items()])
    param_string_md = f"{parameters_md}\n" if parameters_md else ""
    param_string_plain = f"{parameters_plain}\n" if parameters_plain else ""
    effects_md = "".join([f"**{item['type']}**: {item['text']}" for item in ability_dict["effects"]])
    effects_plain = "".join([f"{item['type']}: {item['text']}" for item in ability_dict["effects"]])
    description_md = f"{param_string_md}{effects_md}"
    description_plain = f"{param_string_plain}{effects_plain}"
    upgrades = ability_dict["upgrades"]
    upgrades_md = f"**Upgrades:**\n" + "".join([f"    {k}. {v}" for k,v, in upgrades.items()])
    upgrades_csv = ",".join([f'"{v}"' for k,v in ability_dict["upgrades"].items()])
    full_text_md = f"{header_md}\n\n{description_md}{upgrades_md}"
    row_record = {
        "Art": ability_dict["art"],
        "Name": name,
        "Type": category,
        "Tags": tags_text,
        "Description": description_plain,
        "Upgrade a": upgrades["a"] if "a" in upgrades.keys() else "",
        "Upgrade b": upgrades["b"] if "b" in upgrades.keys() else "",
        "Upgrade c": upgrades["c"] if "c" in upgrades.keys() else ""
        }
    return {"md": full_text_md, "row_record": row_record}

ability_names = read_yaml("../abilities/combat/index.yml")

arts = ability_names.keys()
abilities = {}
ability_mds = {}
ability_records = {}
ability_frames = {}
for art in arts:
    print(f"Reading {art} abilities")
    abilities[art] = []
    ability_mds[art] = []
    ability_records[art] = []
    for name in ability_names[art]:
        print(f"- Reading {name}")
        ability = read_ability(name, "combat")
        # print(ability)
        abilities[art] += ability
        ability_strings = format_ability_string(ability)
        # print(ability_strings["md"])
        ability_mds[art] += ability_strings["md"]
        # print(ability_strings["row_record"])
        ability_records[art] += [ability_strings["row_record"]]
    # print(ability_records[art])
    ability_frames[art] = pd.DataFrame(ability_records[art])
    # print(ability_frames[art])
    ability_frames[art].to_csv(f"../abilities/generated/{art}.csv")

pd.concat(ability_frames.values()).to_csv("../abilities/generated/all_combat.csv")
