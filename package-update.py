import subprocess
import logging
import select
import sys

# configure logging
logging.basicConfig(
    filename="update_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def check_for_updates():
    print("Checking for package updates...")

    subprocess.run(["sudo", "apt", "update"], check=True)   

    results = subprocess.run(
        ["sudo", "apt", "list", "--upgradable"],
        capture_output=True,
        text=True,
        check=True
    )

    lines = results.stdout.split("\n")

    packages = []

    for line in lines[1:]:
        if line.strip():
            pkg = line.split("/")[0]
            packages.append(pkg)
    if not packages:
        print("No updates available.")
        return []

    print("Available Updates:\n")

    for i, pkg in enumerate(packages):
        print(f"{i+1}. {pkg}")

    return packages

# Function to install a package
def install_package(package):

    print(f"\nInstalling update for: {package}")

    try:
        result = subprocess.run(
            ["sudo", "apt", "install", "-y", package],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{package} updated successfully.")
            logging.info(f"{package} updated successfully.")

        else:
            print(f"ALERT: Failed to update {package}")
            logging.error(result.stderr)

    except Exception as e:
        print(f"ALERT: Installation error for {package}")
        logging.error(str(e))


# Function to get user choice with timeout
def get_user_choice():

    print("\nUpdate all packages? (y/n)")
    print("Waiting 60 seconds for user input...")

    ready, _, _ = select.select([sys.stdin], [], [], 60)

    if ready:
        choice = sys.stdin.readline().strip()
        return choice
    else:
        print("\nNo input detected within 60 seconds.")
        print("Automatically updating all packages.")
        return "y"


# Function to update packages
def update_packages(packages):

    choice = get_user_choice()

    # update all packages
    if choice.lower() == "y":

        for pkg in packages:
            install_package(pkg)

    # update selected packages
    else:

        print("\nEnter package index numbers separated by comma (example: 1,3,5)")
        print("Waiting 60 seconds for input...")

        ready, _, _ = select.select([sys.stdin], [], [], 60)

        if ready:

            indexes = sys.stdin.readline().strip()

            selected = []

            for i in indexes.split(","):
                try:
                    selected.append(packages[int(i) - 1])
                except:
                    print("Invalid index:", i)

            for pkg in selected:
                install_package(pkg)

        else:

            print("\nNo input received. Updating all packages automatically.")

            for pkg in packages:
                install_package(pkg)


# Main function
def main():

    packages = check_for_updates()

    if packages:
        update_packages(packages)


# start program
if __name__ == "__main__":
    main()

