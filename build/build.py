import os
import pathlib
import shutil

from dotenv import load_dotenv
from pathlib import Path
import configparser

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

load_dotenv()  # Load .env file if present

base_dir = Path(__file__).parent.parent  # Repo root dir
template_dir = base_dir / "templates"
output_dir = base_dir / "output"

jinja_env = Environment(
  loader=FileSystemLoader(template_dir)
)

def validate_config(ini):
  config = configparser.ConfigParser(allow_no_value=True, strict=False)
  config.read_string(ini)
  return ini

# Build the config files
def build():
  # Ensure output directory exists
  if (output_dir.exists()):
    print("Cleaning output directory...")
    shutil.rmtree(output_dir)
  output_dir.mkdir(exist_ok=True)

  templates = [jinja_env.get_template(t) for t in jinja_env.list_templates(["j2"])]
  for template in templates:
    output_file = output_dir / str(template.name).removesuffix(".j2")
    print(f"Generating {output_file}")

    content = validate_config(template.render(ENV=os.environ))
    with open(output_file, "w") as out:
      out.write(content)


if __name__ == '__main__':
  build()
