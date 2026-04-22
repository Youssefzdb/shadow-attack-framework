#!/usr/bin/env python3
"""Reconnaissance & OSINT Module"""
import socket
import subprocess
import json
from utils.logger import Logger

class Recon:
    def __init__(self, target: str, mode: str, logger: Logger):
        self.target = target
        self.mode = mode
        self.logger = logger
        self.results = {}

    def _dns_lookup(self):
        try:
            ip = socket.gethostbyname(self.target)
            self.results["ip"] = ip
            self.logger.success(f"DNS Resolved: {self.target} -> {ip}")
        except Exception as e:
            self.logger.error(f"DNS lookup failed: {e}")

    def _reverse_dns(self, ip: str):
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            self.results["hostname"] = hostname
            self.logger.success(f"Reverse DNS: {ip} -> {hostname}")
        except:
            self.logger.warning("Reverse DNS: no result")

    def _whois(self):
        try:
            result = subprocess.run(["whois", self.target], capture_output=True, text=True, timeout=10)
            self.results["whois"] = result.stdout[:500]
            self.logger.success("WHOIS data retrieved")
        except Exception as e:
            self.logger.warning(f"WHOIS failed: {e}")

    def _active_ping(self):
        try:
            result = subprocess.run(["ping", "-c", "3", self.target], capture_output=True, text=True, timeout=10)
            alive = result.returncode == 0
            self.results["ping"] = "alive" if alive else "unreachable"
            self.logger.success(f"Ping: host is {alive if alive else unreachable}")
        except Exception as e:
            self.logger.warning(f"Ping failed: {e}")

    def run(self):
        self.logger.info(f"[*] Starting {self.mode} recon on {self.target}")
        self._dns_lookup()
        if "ip" in self.results:
            self._reverse_dns(self.results["ip"])
        self._whois()
        if self.mode == "active":
            self._active_ping()
        self.logger.info(f"[*] Recon complete.")
        print(json.dumps(self.results, indent=2))
        return self.results
