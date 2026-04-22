#!/usr/bin/env python3
"""Logger Utility"""

class Logger:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def info(self, msg): print(f"{self.BLUE}[*]{self.RESET} {msg}")
    def success(self, msg): print(f"{self.GREEN}[+]{self.RESET} {msg}")
    def warning(self, msg): print(f"{self.YELLOW}[!]{self.RESET} {msg}")
    def error(self, msg): print(f"{self.RED}[-]{self.RESET} {msg}")
    def debug(self, msg):
        if self.verbose:
            print(f"[DEBUG] {msg}")
