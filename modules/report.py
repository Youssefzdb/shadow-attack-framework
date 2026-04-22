import json
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self, input_file, output_file, fmt, logger):
        self.input_file = input_file
        self.output_file = output_file
        self.fmt = fmt
        self.logger = logger

    def run(self):
        self.logger.info(f"[*] Generating {self.fmt.upper()} report from {self.input_file}")
        try:
            with open(self.input_file) as f:
                data = json.load(f)
        except Exception as e:
            self.logger.error(f"[!] Failed to read input: {e}")
            return

        if self.fmt == "html":
            self._generate_html(data)
        elif self.fmt == "json":
            self._generate_json(data)

    def _generate_html(self, data):
        html = f"""<!DOCTYPE html>
<html>
<head><title>Pentest Report — Shadow Attack Framework</title>
<style>
body {{ font-family: monospace; background: #0d0d0d; color: #00ff41; padding: 30px; }}
h1 {{ color: #ff0040; }} table {{ width: 100%; border-collapse: collapse; }}
th, td {{ border: 1px solid #333; padding: 8px; text-align: left; }}
th {{ background: #1a1a1a; }} .critical {{ color: #ff0040; }} .high {{ color: #ff8c00; }}
</style></head>
<body>
<h1>🔴 Penetration Test Report</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<p>Author: Shadow Core</p>
<h2>Findings</h2>
<pre>{json.dumps(data, indent=2)}</pre>
</body></html>"""
        with open(self.output_file, "w") as f:
            f.write(html)
        self.logger.info(f"[+] Report saved to {self.output_file}")

    def _generate_json(self, data):
        data["generated_at"] = datetime.now().isoformat()
        data["author"] = "Shadow Core"
        with open(self.output_file, "w") as f:
            json.dump(data, f, indent=2)
        self.logger.info(f"[+] JSON report saved to {self.output_file}")
