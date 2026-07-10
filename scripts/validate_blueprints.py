from pathlib import Path
import sys
import yaml

BLUEPRINTS = list(Path(".").rglob("*.yaml"))

class BlueprintLoader(yaml.SafeLoader):
    pass

BlueprintLoader.add_constructor(
    "!input",
    lambda loader, node: loader.construct_scalar(node)
)

errors = []

for file in BLUEPRINTS:

    if ".github" in str(file):
        continue

    try:
        with open(file, encoding="utf-8") as f:
            content = yaml.load(f, Loader=BlueprintLoader)

        if not isinstance(content, dict):
            errors.append(f"{file}: Invalid root structure")
            continue

        if "blueprint" not in content:
            continue

        bp = content["blueprint"]

        required = [
            "name",
            "description",
            "domain"
        ]

        for field in required:
            if field not in bp:
                errors.append(
                    f"{file}: Missing blueprint.{field}"
                )

        inputs = content.get("input", {})

        for name, cfg in inputs.items():
            if not isinstance(cfg, dict):
                continue

            if "name" not in cfg:
                errors.append(
                    f"{file}: Input '{name}' missing name"
                )

            if "selector" not in cfg:
                errors.append(
                    f"{file}: Input '{name}' missing selector"
                )

    except Exception as e:
        errors.append(f"{file}: {e}")

if errors:
    print("\n".join(errors))
    sys.exit(1)

print("Blueprint validation successful.")
