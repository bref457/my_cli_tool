import os
import sys

def list_directory_contents(path):
    """Lists the contents of a given directory."""
    try:
        with os.scandir(path) as entries:
            print(f"Contents of '{path}':")
            for entry in entries:
                print(f"- {entry.name}{'/' if entry.is_dir() else ''}")
    except FileNotFoundError:
        print(f"Error: Directory '{path}' not found.")
    except NotADirectoryError:
        print(f"Error: '{path}' is not a directory.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def create_folder(path, folder_name):
    """Creates a new folder at the specified path."""
    new_folder_path = os.path.join(path, folder_name)
    try:
        os.makedirs(new_folder_path)
        print(f"Folder '{folder_name}' created successfully at '{path}'.")
    except FileExistsError:
        print(f"Error: Folder '{folder_name}' already exists at '{path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def create_empty_file(path, file_name):
    """Creates a new empty file at the specified path."""
    new_file_path = os.path.join(path, file_name)
    try:
        with open(new_file_path, 'w') as f:
            pass # Create an empty file
        print(f"Empty file '{file_name}' created successfully at '{path}'.")
    except FileExistsError:
        print(f"Error: File '{file_name}' already exists at '{path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def display_help():
    """Displays the help message."""
    print("Simple CLI File Manager")
    print("Usage: python main.py <command> [arguments]")
    print("\nCommands:")
    print("  list [path]        - List contents of a directory. Defaults to current directory.")
    print("  mkdir <path> <name> - Create a new folder.")
    print("  touch <path> <name> - Create a new empty file.")
    print("  help               - Display this help message.")

def main():
    if len(sys.argv) < 2:
        display_help()
        return

    command = sys.argv[1]

    if command == "list":
        path = sys.argv[2] if len(sys.argv) > 2 else "."
        list_directory_contents(path)
    elif command == "mkdir":
        if len(sys.argv) < 4:
            print("Usage: mkdir <path> <name>")
            return
        path = sys.argv[2]
        name = sys.argv[3]
        create_folder(path, name)
    elif command == "touch":
        if len(sys.argv) < 4:
            print("Usage: touch <path> <name>")
            return
        path = sys.argv[2]
        name = sys.argv[3]
        create_empty_file(path, name)
    elif command == "help":
        display_help()
    else:
        print(f"Unknown command: {command}")
        display_help()

if __name__ == "__main__":
    main()
