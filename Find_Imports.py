import os
import re


def find_imports(directory):
    imports = set()
    import_pattern = re.compile(r'^\s*(?:import|from)\s+(\S+)', re.IGNORECASE)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    for line in f:
                        match = import_pattern.match(line)
                        if match:
                            module = match.group(1).split('.')[0]
                            imports.add(module)

    return imports


if __name__ == "__main__":
    repo_path = '/CodeYou_Capstone'
    modules = find_imports(repo_path)

    for module in sorted(modules):
        print(module)
