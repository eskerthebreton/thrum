from .io import read_string, read_yaml, write_md
from pathlib import Path

class ThrumPage:
    def __init__(self, name, template, bindings, write_path):
        self.name = name
        self.elements = build_elements(template, bindings)
        self.path = write_path
    def to_string(self):
        return "\n\n".join(self.elements)
    def write(self):
        result = self.to_string()
        print(f"Writing page {self.name} to file {self.path}")
        write_md(result, self.path)
        return result

def build_pages(content_config_path, type_mapping_path, write_base_path, write_to_disk = True):
    result = {}
    content_config = read_yaml(content_config_path)
    type_mapping = read_yaml(type_mapping_path)
    templates = {page_type: read_yaml(path) for page_type, path in type_mapping.items()} 
    for page_id, config in content_config.items():
        bindings = config["bindings"]
        page_type = config["template"]
        write_path = Path(write_base_path) / config["page"]
        template = templates[page_type]
        page = ThrumPage(page_id, template, bindings, write_path)
        result[page_id] = page
        if write_to_disk:
            page.write()
    return result

def element_dispatcher(type):
    match type:
        case "navbar":
            return build_navbar
        case "image":
            return build_image
        case "markdown":
            return build_markdown

def build_elements(template, bindings):
    elements = template["elements"]
    results = []
    for element in elements:
        element_type = element["type"]
        parameters = read_parameters(element, bindings)
        builder = element_dispatcher(element_type)
        result = builder(parameters, bindings)
        # print(result)
        results += [result]
    return results
        
def read_parameters(element, bindings):
    result = {}
    for k,v in element["parameters"].items():
        if isinstance(v, str):
            result[k] = v.format(**bindings)
        else:
            result[k] = v
    return result

def build_from_template(template_type, bindings):
    templates = read_yaml("../headers/templates/element_templates.yml")
    template_path = templates[template_type]
    result = read_string(f"../headers/templates/{template_path}").format(**bindings)
    return result

def build_navbar(parameters, bindings):
    links = parameters["links"]
    for link in links:
        link['preface'] = f"**{link['preface']}**:" if link['preface'] else ""
    navlinks = "|".join(
        [f"{link['preface']} [{link['link_text']}]({link['link_slug']})" for link in links]) + "|"
    separator = "|".join([f"------" for link in links]) + "|"
    result = navlinks + "\n" + separator
    return(result)

def build_image(parameters, bindings):
    # bound_parameters = {}
    # for k,v in bound_parameters.items():
    #     bound_parameters[k] = v.format(**bindings)
    result = build_from_template("image", parameters)
    return result

def build_markdown(parameters, bindings):
    result = read_string(parameters["path"]).format(**bindings)
    return result
