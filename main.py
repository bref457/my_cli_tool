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

def delete_item(path):
    """Deletes a file or an empty directory at the specified path."""
    try:
        if os.path.isfile(path):
            os.remove(path)
            print(f"File '{path}' deleted successfully.")
        elif os.path.isdir(path):
            os.rmdir(path)
            print(f"Empty directory '{path}' deleted successfully.")
        else:
            print(f"Error: '{path}' is neither a file nor an empty directory.")
    except FileNotFoundError:
        print(f"Error: '{path}' not found.")
    except OSError as e:
        print(f"Error deleting '{path}': {e}. Make sure the directory is empty if you are trying to delete a folder.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def rename_item(old_path, new_path):
    """Renames or moves a file or directory."""
    try:
        os.rename(old_path, new_path)
        print(f"'{old_path}' successfully renamed/moved to '{new_path}'.")
    except FileNotFoundError:
        print(f"Error: '{old_path}' not found.")
    except FileExistsError:
        print(f"Error: '{new_path}' already exists.")
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
    print("  rm <path>          - Delete a file or an empty directory.")
    print("  mv <old_path> <new_path> - Rename or move a file or directory.")
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
    elif command == "rm":
        if len(sys.argv) < 3:
            print("Usage: rm <path>")
            return
        path = sys.argv[2]
        delete_item(path)
    elif command == "mv":
        if len(sys.argv) < 4:
            print("Usage: mv <old_path> <new_path>")
            return
        old_path = sys.argv[2]
        new_path = sys.argv[3]
        rename_item(old_path, new_path)
    elif command == "help":
        display_help()
    else:
        print(f"Unknown command: {command}")
        display_help()

if __name__ == "__main__":
    main()
