import os
import shutil
import sys

# ANSI escape codes for colors and styles
class Style:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def get_recent_path():
    """Get Windows Recent Items folder path safely."""
    appdata = os.getenv('APPDATA')

    if not appdata:
        print(Style.RED + "ERROR: APPDATA environment variable not found." + Style.END)
        sys.exit(1)

    return os.path.join(appdata, r"Microsoft\Windows\Recent")


def delete_recent_items():
    recent_path = get_recent_path()

    # Ensure folder exists
    if not os.path.isdir(recent_path):
        print(Style.RED + f"Recent Items folder not found at:\n{recent_path}" + Style.END)
        sys.exit(1)

    try:
        contents = os.listdir(recent_path)
    except PermissionError:
        print(Style.RED + "Access denied: Cannot access Recent folder. Try running as Administrator." + Style.END)
        sys.exit(1)
    except Exception as e:
        print(Style.RED + f"Unexpected error reading folder: {e}" + Style.END)
        sys.exit(1)

    if not contents:
        print(Style.GREEN + "Recent Items directory is already empty." + Style.END)
        return

    print(Style.BLUE + f"Found {len(contents)} recent item(s). Deleting..." + Style.END)

    deleted = 0
    failed = 0

    for item in contents:
        item_path = os.path.join(recent_path, item)

        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

            deleted += 1

        except PermissionError:
            print(Style.RED + f"Access denied: Could not delete {item}" + Style.END)
            failed += 1
        except Exception as e:
            print(Style.RED + f"Error deleting {item}: {e}" + Style.END)
            failed += 1

    print(Style.GREEN + f"\nDeleted: {deleted}" + Style.END)

    if failed:
        print(Style.RED + f"Failed: {failed}" + Style.END)
    else:
        print(Style.GREEN + "All recent items successfully deleted." + Style.END)


if __name__ == "__main__":
    delete_recent_items()