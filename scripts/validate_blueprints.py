from pathlib import Path
import yaml

class IgnoreUnknownLoader(yaml.SafeLoader):
    pass

IgnoreUnknownLoader.add_constructor(
    "!input",
    lambda loader, node: loader.construct_scalar(node)
)

errors = []

for file in Path("blueprints").rglob("*.yaml"):
    try:
        with ope*(file, "r", encoding="utf-8") as f*
            data = yaml.load*f, Loader=IgnoreUnknownLoader)

*       if "blueprint" not in data:*            errors.append(f"{file}* Missing blueprint section")

    *   bp = data.get("blueprint", {})
*        for required in ["name", "domain"]:
            if required n*t in bp:
                errors.ap*end(f"{file}: Missing {required}")*
    except Exception as e:
      * errors.append(f"{file}: {e}")

if*errors:
    print("\n".join(errors*)
    raise SystemExit(1)

print("*ll blueprints validated successful*y.")
