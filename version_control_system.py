import os
import shutil
import time
import filecmp
import difflib

# Folder to store versions
VERSION_FOLDER = "versions"
os.makedirs(VERSION_FOLDER, exist_ok=True)


# Save file version
def save_version(file_path):

    if not os.path.isfile(file_path):
        print("File does not exist.")
        return

    filename = os.path.basename(file_path)

    timestamp = int(time.time())
    version_name = f"{filename}_v{timestamp}"

    version_path = os.path.join(VERSION_FOLDER, version_name)

    shutil.copy(file_path, version_path)

    print("Version saved:", version_name)


# Restore a file version
def restore_version(version_file, original_dir):

    version_path = os.path.join(VERSION_FOLDER, version_file)

    if not os.path.isfile(version_path):
        print("Version file not found.")
        return

    original_file = version_file.split("_v")[0]
    restore_path = os.path.join(original_dir, original_file)

    shutil.copy(version_path, restore_path)

    print("File restored to:", restore_path)


# Compare versions (handles text + binary files)
def compare_versions(file1, file2):

    path1 = os.path.join(VERSION_FOLDER, file1)
    path2 = os.path.join(VERSION_FOLDER, file2)

    if not os.path.exists(path1) or not os.path.exists(path2):
        print("One or both version files not found.")
        return

    try:
        # Try reading as text
        with open(path1, "r") as f1, open(path2, "r") as f2:

            diff = difflib.unified_diff(
                f1.readlines(),
                f2.readlines(),
                fromfile=file1,
                tofile=file2
            )

            result = list(diff)

            if result:
                print("Differences found:\n")
                print("".join(result))
            else:
                print("Files are identical.")

    except UnicodeDecodeError:

        print("Binary files detected (PDF, images, etc.).")

        if filecmp.cmp(path1, path2):
            print("Files are identical.")
        else:
            print("Files are different.")


# Cleanup old versions
def cleanup_versions(keep_last):

    files = sorted(os.listdir(VERSION_FOLDER))

    if len(files) <= keep_last:
        print("No old versions to delete.")
        return

    old_files = files[:-keep_last]

    for f in old_files:
        os.remove(os.path.join(VERSION_FOLDER, f))
        print("Deleted old version:", f)


# Main Menu
while True:

    print("\n--- File Version Control ---")
    print("1. Save file version")
    print("2. Restore version")
    print("3. Compare versions")
    print("4. Cleanup old versions")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":

        path = input("Enter file path: ")
        save_version(path)

    elif choice == "2":

        version = input("Enter version filename: ")
        directory = input("Enter original directory: ")

        restore_version(version, directory)

    elif choice == "3":

        v1 = input("Enter first version file: ")
        v2 = input("Enter second version file: ")

        compare_versions(v1, v2)

    elif choice == "4":

        n = int(input("Keep last how many versions? "))
        cleanup_versions(n)

    elif choice == "5":

        print("Exiting program.")
        break

    else:

        print("Invalid choice.")