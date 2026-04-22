import socket
import threading
from queue import Queue

class PortScanner:
    def __init__(self, target, ports, threads, logger):
        self.target = target
        self.ports = self._parse_ports(ports)
        self.threads = threads
        self.logger = logger
        self.open_ports = []
        self.queue = Queue()

    def _parse_ports(self, port_range):
        start, end = port_range.split("-")
        return range(int(start), int(end) + 1)

    def _scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((self.target, port))
            sock.close()
            if result == 0:
                self.open_ports.append(port)
                service = self._detect_service(port)
                self.logger.info(f"[OPEN] {self.target}:{port} ({service})")
        except Exception:
            pass

    def _detect_service(self, port):
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
            443: "HTTPS", 445: "SMB", 3306: "MySQL",
            3389: "RDP", 5432: "PostgreSQL", 6379: "Redis",
            8080: "HTTP-Alt", 8443: "HTTPS-Alt"
        }
        return services.get(port, "Unknown")

    def _worker(self):
        while not self.queue.empty():
            port = self.queue.get()
            self._scan_port(port)
            self.queue.task_done()

    def run(self):
        self.logger.info(f"[*] Scanning {self.target} — Ports: {self.ports.start}-{self.ports.stop - 1}")
        for port in self.ports:
            self.queue.put(port)
        workers = []
        for _ in range(min(self.threads, len(self.ports))):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            t.start()
            workers.append(t)
        self.queue.join()
        self.logger.info(f"[+] Scan complete. Open ports: {self.open_ports}")
        return self.open_ports
