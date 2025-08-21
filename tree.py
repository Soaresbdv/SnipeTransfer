import os

# Lista de extensões e nomes de arquivos que você considera inúteis
IGNORED_EXTENSIONS = {'.pyc', '.tmp', '.log'}
IGNORED_FILENAMES = {'Thumbs.db', '.DS_Store'}
IGNORED_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', '.idea', '.vscode'}

def print_tree(root_path, prefix=""):
    try:
        entries = sorted(os.listdir(root_path))
    except PermissionError:
        print(f"{prefix}[Permission Denied]")
        return

    for index, entry in enumerate(entries):
        path = os.path.join(root_path, entry)

        # Verificações de arquivos/pastas ignoradas
        if entry in IGNORED_FILENAMES:
            continue
        if os.path.isdir(path) and entry in IGNORED_DIRS:
            continue
        if os.path.isfile(path) and os.path.splitext(entry)[1] in IGNORED_EXTENSIONS:
            continue

        connector = "└── " if index == len(entries) - 1 else "├── "
        print(prefix + connector + entry)

        if os.path.isdir(path):
            extension = "    " if index == len(entries) - 1 else "│   "
            print_tree(path, prefix + extension)

if __name__ == "__main__":
    ROOT_DIR = "."  # ou substitua por outro caminho ex: "/home/user/projeto"
    print(f"Tree of: {os.path.abspath(ROOT_DIR)}\n")
    print_tree(ROOT_DIR)
