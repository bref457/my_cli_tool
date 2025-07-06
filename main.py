import os
import sys
import shutil
import difflib
import re
import hashlib
import psutil
import subprocess

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

def delete_item(path, recursive=False):
    """Deletes a file or a directory. Can delete non-empty directories if recursive is True."""
    try:
        if os.path.isfile(path):
            os.remove(path)
            print(f"File '{path}' deleted successfully.")
        elif os.path.isdir(path):
            if recursive:
                shutil.rmtree(path)
                print(f"Directory '{path}' and its contents deleted successfully (recursively).")
            else:
                os.rmdir(path)
                print(f"Empty directory '{path}' deleted successfully.")
        else:
            print(f"Error: '{path}' is neither a file nor a directory.")
    except FileNotFoundError:
        print(f"Error: '{path}' not found.")
    except OSError as e:
        print(f"Error deleting '{path}': {e}. Make sure the directory is empty or use -r for recursive deletion.")
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

def display_file_content(path):
    """Displays the content of a given file."""
    try:
        with open(path, 'r') as f:
            print(f"Content of '{path}':")
            print(f.read())
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
    except IsADirectoryError:
        print(f"Error: '{path}' is a directory, not a file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def find_files(directory, search_term):
    """Recursively searches for files by name within a given directory."""
    found_files = []
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                if search_term in file:
                    found_files.append(os.path.join(root, file))
        if found_files:
            print(f"Found files matching '{search_term}' in '{directory}':")
            for f in found_files:
                print(f"- {f}")
        else:
            print(f"No files matching '{search_term}' found in '{directory}'.")
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def copy_item(source_path, destination_path):
    """Copies a file or a directory."""
    try:
        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)
            print(f"File '{source_path}' copied to '{destination_path}'.")
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path)
            print(f"Directory '{source_path}' copied to '{destination_path}'.")
        else:
            print(f"Error: '{source_path}' is neither a file nor a directory.")
    except FileNotFoundError:
        print(f"Error: Source '{source_path}' not found.")
    except FileExistsError:
        print(f"Error: Destination '{destination_path}' already exists. Cannot copy to an existing directory.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def edit_file_content(path, content, append=False):
    """Writes content to a file. Overwrites by default, appends if append is True."""
    mode = 'a' if append else 'w'
    try:
        with open(path, mode) as f:
            f.write(content + '\n')
        print(f"Content written to '{path}' (mode: {'append' if append else 'overwrite'}).")
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def change_permissions(path, mode_str):
    """Changes the permissions of a file or directory."""
    try:
        mode = int(mode_str, 8) # Convert octal string to integer
        os.chmod(path, mode)
        print(f"Permissions of '{path}' changed to {mode_str}.")
    except FileNotFoundError:
        print(f"Error: '{path}' not found.")
    except ValueError:
        print(f"Error: Invalid mode '{mode_str}'. Please use an octal number (e.g., 755).")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def zip_item(source_path, output_filename):
    """Compresses a file or directory into a zip archive."""
    try:
        base_name = os.path.basename(output_filename)
        archive_name = shutil.make_archive(os.path.join(os.path.dirname(output_filename), base_name.split('.')[0]), 'zip', root_dir=os.path.dirname(source_path), base_dir=os.path.basename(source_path))
        print(f"'{source_path}' compressed to '{archive_name}'.")
    except FileNotFoundError:
        print(f"Error: Source '{source_path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def unzip_item(source_path, destination_path):
    """Decompresses a zip archive."""
    try:
        shutil.unpack_archive(source_path, destination_path, 'zip')
        print(f"'{source_path}' decompressed to '{destination_path}'.")
    except FileNotFoundError:
        print(f"Error: Archive '{source_path}' not found.")
    except shutil.ReadError:
        print(f"Error: '{source_path}' is not a valid zip archive.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def display_size(path):
    """Displays the size of a file or a directory."""
    try:
        if os.path.isfile(path):
            size = os.path.getsize(path)
            print(f"Size of '{path}': {size} bytes")
        elif os.path.isdir(path):
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
            print(f"Size of directory '{path}': {total_size} bytes")
        else:
            print(f"Error: '{path}' not found or is not a file or directory.")
    except FileNotFoundError:
        print(f"Error: '{path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def compare_files(file1_path, file2_path):
    """Compares two text files and prints the differences."""
    try:
        with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
            diff = difflib.unified_diff(f1.readlines(), f2.readlines(), fromfile=file1_path, tofile=file2_path)
            for line in diff:
                sys.stdout.write(line)
    except FileNotFoundError:
        print(f"Error: One or both files not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def display_metadata(path):
    """Displays metadata of a file or directory."""
    try:
        stats = os.stat(path)
        print(f"Metadata for '{path}':")
        print(f"  Size: {stats.st_size} bytes")
        print(f"  Last modified: {os.path.getmtime(path)}")
        print(f"  Last accessed: {os.path.getatime(path)}")
        print(f"  Creation time: {os.path.getctime(path)}")
        print(f"  Mode: {oct(stats.st_mode)}")
        print(f"  Inode: {stats.st_ino}")
        print(f"  Device: {stats.st_dev}")
        print(f"  Number of links: {stats.st_nlink}")
        print(f"  Owner UID: {stats.st_uid}")
        print(f"  Group GID: {stats.st_gid}")
    except FileNotFoundError:
        print(f"Error: '{path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def grep_file_content(path, pattern):
    """Searches for a pattern within the content of a file."""
    try:
        with open(path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if re.search(pattern, line):
                    print(f"{path}:{line_num}: {line.strip()}")
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def generate_hash(path, algorithm):
    """Generates the hash of a file using the specified algorithm (md5 or sha256)."""
    try:
        hasher = None
        if algorithm == "md5":
            hasher = hashlib.md5()
        elif algorithm == "sha256":
            hasher = hashlib.sha256()
        else:
            print(f"Error: Unsupported hash algorithm '{algorithm}'. Use 'md5' or 'sha256'.")
            return

        with open(path, 'rb') as f:
            while True:
                chunk = f.read(4096) # Read in chunks
                if not chunk:
                    break
                hasher.update(chunk)
        print(f"Hash of '{path}' ({algorithm}): {hasher.hexdigest()}")
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def list_processes():
    """Lists all running processes."""
    print("PID\tName\tCPU%\tMEM%")
    print("--------------------------------------------------")
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            print(f"{proc.info['pid']}\t{proc.info['name']}\t{proc.info['cpu_percent']:.1f}\t{proc.info['memory_percent']:.1f}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print("--------------------------------------------------")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def ping_host(host):
    """Pings a host and displays the output."""
    try:
        # Use platform-specific ping command
        if sys.platform.startswith('win'):
            command = ['ping', '-n', '1', host] # Ping once on Windows
        else:
            command = ['ping', '-c', '1', host] # Ping once on Linux/macOS
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error pinging '{host}': {e.stderr}")
    except FileNotFoundError:
        print(f"Error: 'ping' command not found. Make sure it's in your system's PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def display_sysinfo():
    """Displays detailed system information (CPU, memory, disk, network)."""
    print("\n--- System Information ---")
    # CPU Info
    print(f"CPU Cores: {psutil.cpu_count(logical=False)} (Physical), {psutil.cpu_count(logical=True)} (Logical)")
    print(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")

    # Memory Info
    mem = psutil.virtual_memory()
    print(f"Total Memory: {mem.total / (1024**3):.2f} GB")
    print(f"Available Memory: {mem.available / (1024**3):.2f} GB")
    print(f"Used Memory: {mem.used / (1024**3):.2f} GB ({mem.percent}%) ")

    # Disk Info
    print("\n--- Disk Usage ---")
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            print(f"  {part.device} ({part.mountpoint}): Total={usage.total / (1024**3):.2f} GB, Used={usage.used / (1024**3):.2f} GB, Free={usage.free / (1024**3):.2f} GB ({usage.percent}%) ")
        except Exception:
            continue

    # Network Info
    print("\n--- Network Info ---")
    net_io = psutil.net_io_counters()
    print(f"Bytes Sent: {net_io.bytes_sent / (1024**2):.2f} MB")
    print(f"Bytes Received: {net_io.bytes_recv / (1024**2):.2f} MB")
    print("--------------------------")

def display_help():
    """Displays the help message."""
    print("Simple CLI File Manager")
    print("Usage: python main.py <command> [arguments]")
    print("\nCommands:")
    print("  list [path]        - List contents of a directory. Defaults to current directory.")
    print("  mkdir <path> <name> - Create a new folder.")
    print("  touch <path> <name> - Create a new empty file.")
    print("  rm <path>          - Delete a file or an empty directory.")
    print("  rm -r <path>       - Recursively delete a directory and its contents.")
    print("  mv <old_path> <new_path> - Rename or move a file or directory.")
    print("  cat <path>         - Display the content of a file.")
    print("  find <directory> <search_term> - Search for files by name in a directory.")
    print("  cp <source> <destination> - Copy a file or directory.")
    print("  echo [-a] <path> <content> - Write content to a file. Use -a to append.")
    print("  chmod <path> <mode> - Change permissions of a file or directory (e.g., 755).")
    print("  zip <source> <output_filename> - Compress a file or directory into a zip archive.")
    print("  unzip <source> <destination> - Decompress a zip archive.")
    print("  du <path>          - Display the size of a file or directory.")
    print("  diff <file1> <file2> - Compare two text files.")
    print("  stat <path>        - Display metadata of a file or directory.")
    print("  grep <path> <pattern> - Search for a pattern within the content of a file.")
    print("  hash <path> <algorithm> - Generate hash (md5 or sha256) of a file.")
    print("  ps                 - List running processes.")
    print("  ping <host>        - Ping a host (e.g., google.com or 8.8.8.8).")
    print("  sysinfo            - Display detailed system information.")
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
        if len(sys.argv) > 3 and sys.argv[2] == "-r":
            delete_item(sys.argv[3], recursive=True)
        else:
            delete_item(path)
    elif command == "mv":
        if len(sys.argv) < 4:
            print("Usage: mv <old_path> <new_path>")
            return
        old_path = sys.argv[2]
        new_path = sys.argv[3]
        rename_item(old_path, new_path)
    elif command == "cat":
        if len(sys.argv) < 3:
            print("Usage: cat <path>")
            return
        path = sys.argv[2]
        display_file_content(path)
    elif command == "find":
        if len(sys.argv) < 4:
            print("Usage: find <directory> <search_term>")
            return
        directory = sys.argv[2]
        search_term = sys.argv[3]
        find_files(directory, search_term)
    elif command == "cp":
        if len(sys.argv) < 4:
            print("Usage: cp <source> <destination>")
            return
        source_path = sys.argv[2]
        destination_path = sys.argv[3]
        copy_item(source_path, destination_path)
    elif command == "echo":
        if len(sys.argv) < 4:
            print("Usage: echo [-a] <path> <content>")
            return
        append_mode = False
        start_index = 2
        if sys.argv[2] == "-a":
            append_mode = True
            start_index = 3
        
        if len(sys.argv) < start_index + 2:
            print("Usage: echo [-a] <path> <content>")
            return
        
        path = sys.argv[start_index]
        content = sys.argv[start_index + 1]
        edit_file_content(path, content, append_mode)
    elif command == "chmod":
        if len(sys.argv) < 4:
            print("Usage: chmod <path> <mode>")
            return
        path = sys.argv[2]
        mode_str = sys.argv[3]
        change_permissions(path, mode_str)
    elif command == "zip":
        if len(sys.argv) < 4:
            print("Usage: zip <source> <output_filename>")
            return
        source_path = sys.argv[2]
        output_filename = sys.argv[3]
        zip_item(source_path, output_filename)
    elif command == "unzip":
        if len(sys.argv) < 4:
            print("Usage: unzip <source> <destination>")
            return
        source_path = sys.argv[2]
        destination_path = sys.argv[3]
        unzip_item(source_path, destination_path)
    elif command == "du":
        if len(sys.argv) < 3:
            print("Usage: du <path>")
            return
        path = sys.argv[2]
        display_size(path)
    elif command == "diff":
        if len(sys.argv) < 4:
            print("Usage: diff <file1> <file2>")
            return
        file1_path = sys.argv[2]
        file2_path = sys.argv[3]
        compare_files(file1_path, file2_path)
    elif command == "stat":
        if len(sys.argv) < 3:
            print("Usage: stat <path>")
            return
        path = sys.argv[2]
        display_metadata(path)
    elif command == "grep":
        if len(sys.argv) < 4:
            print("Usage: grep <path> <pattern>")
            return
        path = sys.argv[2]
        pattern = sys.argv[3]
        grep_file_content(path, pattern)
    elif command == "hash":
        if len(sys.argv) < 4:
            print("Usage: hash <path> <algorithm>")
            return
        path = sys.argv[2]
        algorithm = sys.argv[3]
        generate_hash(path, algorithm)
    elif command == "ps":
        list_processes()
    elif command == "ping":
        if len(sys.argv) < 3:
            print("Usage: ping <host>")
            return
        host = sys.argv[2]
        ping_host(host)
    elif command == "sysinfo":
        display_sysinfo()
    elif command == "help":
        display_help()
    else:
        print(f"Unknown command: {command}")
        display_help()

if __name__ == "__main__":
    main()
