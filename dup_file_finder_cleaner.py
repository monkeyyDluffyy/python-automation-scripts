import os
import hashlib
import shutil

# Function to calculate SHA256 checksum
def get_checksum(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


# Function to scan directory and find duplicates
def find_duplicates(directory, min_size):
    checksums = {}
    duplicates = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)

            # Skip files smaller than minimum size
            if os.path.getsize(path) < min_size:
                continue

            checksum = get_checksum(path)

            if checksum in checksums:
                duplicates.append((path, checksum))
            else:
                checksums[checksum] = path

    return checksums, duplicates


# Main program
directory = input("Enter directory path to scan: ")
min_size_mb = float(input("Minimum file size in MB (e.g. 1): "))
min_size = min_size_mb * 1024 * 1024

checksums, duplicates = find_duplicates(directory, min_size)

print("\nDuplicate Files Found:")
for file, checksum in duplicates:
    print(file, " -> ", checksum)

# Option to delete or move duplicates
choice = input("\nDelete duplicates (d), Move duplicates (m), Skip (s): ")

if choice == "d":
    for file, _ in duplicates:
        os.remove(file)
        print("Deleted:", file)

elif choice == "m":
    move_folder = input("Enter folder to move duplicates: ")
    os.makedirs(move_folder, exist_ok=True)

    for file, _ in duplicates:
        shutil.move(file, move_folder)
        print("Moved:", file)


# Create report
with open("duplicate_report.txt", "w") as report:
    for file, checksum in duplicates:
        report.write(f"{file} -> {checksum}\n")

print("\nReport saved as duplicate_report.txt")