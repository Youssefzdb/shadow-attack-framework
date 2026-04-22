import socket
import subprocess

class Recon:
    def __init__(self, target, mode, logger):
        self.target = target
        self.mode = mode
        self.logger = logger

    def resolve_dns(self):
        try:
            ip = socket.gethostbyname(self.target)
            self.logger.info(f"[DNS] {self.target} -> {ip}")
            return ip
        except Exception as e:
            self.logger.error(f"[DNS] Failed: {e}")
            return None

    def whois_lookup(self):
        self.logger.info(f"[WHOIS] Querying {self.target}...")
        try:
            result = subprocess.run(["whois", self.target], capture_output=True, text=True, timeout=10)
            lines = [l for l in result.stdout.splitlines() if l.strip() and not l.startswith("%")][:20]
            for line in lines:
                self.logger.info(f"  {line}")
        except FileNotFoundError:
            self.logger.warning("[WHOIS] whois not installed")
        except Exception as e:
            self.logger.error(f"[WHOIS] Error: {e}")

    def banner_grab(self, port=80):
        try:
            s = socket.socket()
            s.settimeout(3)
            s.connect((self.target, port))
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024).decode(errors="ignore")
            self.logger.info(f"[BANNER] Port {port}: {banner[:200]}")
            s.close()
        except Exception as e:
            self.logger.warning(f"[BANNER] Port {port}: {e}")

    def run(self):
        self.logger.info(f"[*] Starting {'passive' if self.mode == 'passive' else 'active'} recon on {self.target}")
        ip = self.resolve_dns()
        self.whois_lookup()
        if self.mode == "active" and ip:
            for port in [80, 443, 22, 21]:
                self.banner_grab(port)
        self.logger.info("[+] Recon complete")
