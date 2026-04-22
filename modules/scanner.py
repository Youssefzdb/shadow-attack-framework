#!/usr/bin/env python3
"""Port & Service Scanner Module"""
import socket
import threading
from utils.logger import Logger

class PortScanner:
    def __init__(self, target: str, ports: str, threads: int, logger: Logger):
        self.target = target
        self.ports = self._parse_ports(ports)
        self.threads = threads
        self.logger = logger
        self.open_ports = []
        self.lock = threading.Lock()

    def _parse_ports(self, port_range: str):
        if "-" in port_range:
            start, end = port_range.split("-")
            return range(int(start), int(end)+1)
        return [int(p) for p in port_range.split(",")]

    def _scan_port(self, port: int):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                with self.lock:
                    self.open_ports.append((port, service))
                self.logger.success(f"Port {port}/tcp OPEN [{service}]")
            sock.close()
        except Exception:
            pass

    def run(self):
        self.logger.info(f"[*] Scanning {self.target} ...")
        threads = []
        for port in self.ports:
            t = threading.Thread(target=self._scan_port, args=(port,))
            threads.append(t)
            t.start()
            if len(threads) >= self.threads:
                for t in threads:
                    t.join()
                threads = []
        for t in threads:
            t.join()
        self.logger.info(f"[*] Scan complete. {len(self.open_ports)} open ports found.")
        return self.open_ports
