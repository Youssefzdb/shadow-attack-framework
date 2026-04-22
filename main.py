#!/usr/bin/env python3
"""
Shadow Attack Framework v1.0
Advanced Network Attack Simulation & Penetration Testing Toolkit
Author: Shadow Core
GitHub: https://github.com/Youssefzdb/shadow-attack-framework
"""

import argparse
import sys
import os
from modules.scanner import PortScanner
from modules.recon import Recon
from modules.bruteforce import BruteForce
from modules.report import ReportGenerator
from utils.banner import print_banner
from utils.logger import Logger

def main():
    print_banner()
    parser = argparse.ArgumentParser(
        description="Shadow Attack Framework — Penetration Testing Toolkit",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="module")

    # Recon
    r = subparsers.add_parser("recon", help="Passive/Active Reconnaissance")
    r.add_argument("--target", required=True, help="Target IP or domain")
    r.add_argument("--mode", choices=["passive","active"], default="passive")

    # Scanner
    s = subparsers.add_parser("scan", help="Port & Service Scanner")
    s.add_argument("--target", required=True)
    s.add_argument("--ports", default="1-1024")
    s.add_argument("--threads", type=int, default=100)

    # Bruteforce
    b = subparsers.add_parser("brute", help="Credential Brute Force Simulation")
    b.add_argument("--target", required=True)
    b.add_argument("--service", choices=["ssh","ftp","http"], required=True)
    b.add_argument("--wordlist", required=True)

    # Report
    rp = subparsers.add_parser("report", help="Generate Pentest Report")
    rp.add_argument("--input", required=True)
    rp.add_argument("--output", default="report.html")

    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if not args.module:
        parser.print_help()
        sys.exit(0)

    log = Logger(args.verbose if hasattr(args,"verbose") else False)

    if args.module == "recon":
        Recon(args.target, args.mode, log).run()
    elif args.module == "scan":
        PortScanner(args.target, args.ports, args.threads, log).run()
    elif args.module == "brute":
        BruteForce(args.target, args.service, args.wordlist, log).run()
    elif args.module == "report":
        ReportGenerator(args.input, args.output, log).run()

if __name__ == "__main__":
    main()

