import os 

def send_cls():
    """Clears the terminal, wether its """
    if os.name == 'posix': # Linux, macOS, WSL
        print("\033[H\033[2J", end="")
    elif os.name == 'nt': # Windows CMD, pwsh 
        if "TERM" in os.environ or "WT_SESSION" in os.environ:
            print("\033[H\033[2J", end="")
        else:
            os.system('cls')
