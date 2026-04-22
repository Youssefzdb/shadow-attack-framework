#!/usr/bin/env python3
"""
Shadow Attack Framework
Advanced Network Attack Simulation & Penetration Testing Toolkit
Author: Shadow Core
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.scanner import PortScanner
from modules.recon import Recon
from modules.exploits import ExploitEngine
from modules.report import ReportGenerator
from utils.banner import print_banner
from utils.logger import setup_logger

def main():
    print_banner()
    parser = argparse.ArgumentParser(
        description="Shadow Attack Framework — Penetration Testing Toolkit",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="module", help="Module to run")

    recon_parser = subparsers.add_parser("recon", help="Reconnaissance & OSINT")
    recon_parser.add_argument("--target", required=True, help="Target IP or domain")
    recon_parser.add_argument("--mode", choices=["passive", "active"], default="passive")

    scan_parser = subparsers.add_parser("scan", help="Port & Service Scanner")
    scan_parser.add_argument("--target", required=True, help="Target IP or CIDR")
    scan_parser.add_argument("--ports", default="1-1024", help="Port range")
    scan_parser.add_argument("--threads", type=int, default=100)

    exploit_parser = subparsers.add_parser("exploit", help="Exploit Simulation")
    exploit_parser.add_argument("--target", required=True, help="Target IP")
    exploit_parser.add_argument("--vuln", required=True, help="CVE ID (e.g. CVE-2021-44228)")
    exploit_parser.add_argument("--dry-run", action="store_true", help="Simulate only")

    report_parser = subparsers.add_parser("report", help="Generate Pentest Report")
    report_parser.add_argument("--input", required=True, help="Scan results JSON")
    report_parser.add_argument("--output", default="report.html")
    report_parser.add_argument("--format", choices=["html", "json"], default="html")

    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if not args.module:
        parser.print_help()
        sys.exit(0)

    logger = setup_logger(getattr(args, 'verbose', False))

    if args.module == "recon":
        Recon(args.target, args.mode, logger).run()
    elif args.module == "scan":
        PortScanner(args.target, args.ports, args.threads, logger).run()
    elif args.module == "exploit":
        ExploitEngine(args.target, args.vuln, args.dry_run, logger).run()
    elif args.module == "report":
        ReportGenerator(args.input, args.output, args.format, logger).run()

if __name__ == "__main__":
    main()
