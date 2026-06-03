import pandas as pd
from pydash import get
from .util import to_plain
from .io import read_yaml, write_md, read_ability

class ThrumAbility:
    def __init__(self, vals: dict):
        self.spec = vals
        self.name = get(vals, "name")
        self.art = get(vals, "art")
        self.index = get(vals, "index", default = 999)
        self.category = get(vals, "type")
        self.tags = get(vals, "tags", default = [])
        self.parameters = get(vals, "parameters", default = {})
        self.effects = get(vals, "effects", default = [])
        self.upgrades = get(vals, "upgrades", default = {})
        self.md = ThrumAbilityMarkdown(self)
        self.plain_text = ThrumAbilityPlainText(self)
    def markdown(self):
        return self.md.text()
    def plaintext(self):
        return self.plain_text.text()
    def table_entry(self):
        result = {
          "Art": self.art,
          "Ability": self.name,
          "Type": self.category,
          "Tags": ", ".join(self.tags),
          "Description": to_plain(self.plaintext()),
          "Upgrade a": to_plain(self.upgrades["a"]) if "a" in self.upgrades else "",
          "Upgrade b": to_plain(self.upgrades["b"]) if "b" in self.upgrades else "",
          "Upgrade c": to_plain(self.upgrades["c"]) if "c" in self.upgrades else ""    
        }
        return result
        

class ThrumAbilityMarkdown:
    def __init__(self, ability: ThrumAbility):
        self.header = f"## {ability.name}"
        self.tags = ", ".join(ability.tags)        
        self.parenthetical = f" ({self.tags})" if self.tags else ""
        self.category = f"**Type:** {ability.category}{self.parenthetical}"
        self.parameters = "\n".join([f"**{k}**: {v}" for k,v in ability.parameters.items()])
        self.param_string = f"{self.parameters}\n" if self.parameters else ""
        self.effects = "".join([f"**{item['type']}**: {item['text']}" for item in ability.effects])
        self.upgrades = f"**Upgrades:**\n" + "".join([f"    {k}. {v}" for k,v, in ability.upgrades.items()])        
    def text(self):
        return f"{self.header}\n\n{self.param_string}{self.effects}{self.upgrades}"

class ThrumAbilityPlainText:
    def __init__(self, ability: ThrumAbility):
        self.parameters = "\n".join([f"{k}: {v}" for k,v in ability.parameters.items()])
        self.param_string = f"{self.parameters}\n" if self.parameters else ""
        self.effects = "".join([f"{item['type']}: {item['text']}" for item in ability.effects])
        self.upgrades = ",".join([f'"{v}"' for k,v in ability.upgrades.items()])
    def text(self):
        return f"{self.param_string}{self.effects}"

def read_all_abilities(config_file):
    index = read_yaml(config_file)
    result = {
        ability_type: {
            art: read_art_abilities(abilities, art, ability_type)
            for art, ability_set in abilities.items()
        } for ability_type, abilities in index.items()
    }
    return result

def read_art_abilities(index, art, ability_type):
    print(f"Reading {art} abilities")
    ability_specs = {name: read_ability(name, ability_type) for name in index[art]}
    result = {name: ThrumAbility(spec) for name,spec in ability_specs.items()}
    return result
    

def format_all_abilities(config_file):
    abilities = read_all_abilities(config_file)
    for ability_type, collection in abilities.items():
        ability_mds = {
            art: [ability.markdown() for name, ability in ability_set.items()]
            for art, ability_set in collection.items()
        }
        ability_records = {
            art: [ability.table_entry() for name, ability in ability_set.items()]
            for art, ability_set in collection.items()
        }
        ability_frames = {
            art: pd.DataFrame(record)
            for art, record in ability_records.items()
        }
        csvs = {
            art: frame.to_csv(f"../abilities/generated/{art}.csv")
            for art, frame in ability_frames.items()
        }
        mds = {
            art: write_md("\n\n".join(desc), f"../abilities/generated/{art}.md")
            for art, desc in ability_mds.items()
        }
        pd.concat(ability_frames.values()).to_csv(
            f"../abilities/generated/all_{ability_type}.csv",
            index=False
        )
    
