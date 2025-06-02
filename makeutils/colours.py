class Colours:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def coloured_print(message, color=Colours.WHITE, end='\n', use_colours=True):
    if use_colours:
        print(f"{color}{message}{Colours.END}", end=end)
    else:
        print(message, end=end)
