import sys
from services import *
from utils import *

def print_help_message():
    """
    Prints help message
    """
    print("usage: cli.py [-h] {execute,view} ...")
    print()
    print("CLI tool")
    print()
    print("positional arguments:")
    print(" {execute,view}")
    print("  execute     Read entire stdin as input script")
    print("  view        View times by ID")
    print()
    print("options:")
    print(" -h, --help   show this help message and exit")

if __name__ == "__main__":
    """
    Reads arguments and calls the appropriate service
    """
    args = sys.argv[1:]
    num_args = len(args)

    if num_args == 0:
        print_help_message()
    elif num_args == 1:
        arg = args[0]
        if arg in ("-h", "--help"):
            print_help_message()
        elif arg == "execute":
            # Extract all lines
            lines = [remove_whitespace(line) for line in sys.stdin]
            # Execute and print id
            id = execute(lines)
            print("Script successfully executed:", id)
        else:
            print("Undefined command!")
            print_help_message()
    elif num_args >= 3 and args[0] == "view" and args[1] == "--id":
        # Extract id and item names
        id = args[2]
        series_names = args[3:]
        # Fetch and display items
        series = view(id, series_names)
        for series_name, series_value in series.items():
            print(series_name, ":")
            print("   ", series_value)
    else:
        print("Undefined command!")
        print_help_message()