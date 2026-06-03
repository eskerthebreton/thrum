from utils.abilities import format_all_abilities
from utils.pages import build_pages
from dotenv import dotenv_values

env = dotenv_values()
format_all_abilities(env["ABILITY_LIST"])

pages = build_pages(
    content_config_path = env["ABILITY_FORMATS"],
    type_mapping_path = env["PAGE_TEMPLATES"],
    write_base_path = env["PAGE_WRITE_PATH"])

