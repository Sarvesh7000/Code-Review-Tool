import os
import re
import json
import subprocess
import pandas as pd
from pathlib import Path

# --- Constants for Header Validation ---
SUPPORTED_EXTENSIONS = {
    '.js': 'javascript', '.ts': 'typescript', '.java': 'java',
    '.py': 'python', '.go': 'go', '.h': 'header',
}

REQUIRED_FIELDS = {
    'purpose': r'(?i)(purpose|description)\s*:\s*(.+)',
    'author': r'(?i)author\s*:\s*(.+)',
    'date': r'(?i)date\s*:\s*(.+)',
    'modified': r'(?i)(modified\s*by|modified|changes?)\s*:\s*(.+)',
}

class CodeReviewer:
    def __init__(self, target_path):
        self.script_dir = Path(__file__).parent.resolve()
        self.rules_dir = self.script_dir / "rules"
        self.common_rules = self.rules_dir / "common-rules.yml"
        self.target_path = Path(target_path).resolve()
        
        self.results = []
        self.rule_map = {
            '.js': self.rules_dir / 'javascript-rules.yml',
            '.py': self.rules_dir / 'python-rules.yml',
            '.go': self.rules_dir / 'go-rules.yml',
            '.java': self.rules_dir / 'java-rules.yml'
        }

    def extract_header(self, file_path):
        """Extracts the first 50 lines to check for header fields."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return '\n'.join(content.split('\n')[:50])
        except Exception:
            return ""

    def check_header(self, file_path):
        """Validates the header and appends errors to results if fields are missing."""
        if file_path.suffix not in SUPPORTED_EXTENSIONS:
            return

        header_text = self.extract_header(file_path)
        missing_fields = []

        for field_name, pattern in REQUIRED_FIELDS.items():
            if not re.search(pattern, header_text, re.MULTILINE | re.IGNORECASE):
                missing_fields.append(field_name)

        if missing_fields:
            self.results.append({
                "Timestamp": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                "File": file_path.name,
                "Line": 1,
                "Rule ID": "HEADER-CHECK",
                "Severity": "ERROR",
                "Message": f"Missing mandatory fields: {', '.join(missing_fields)}"
            })

    def review_file(self, file_path):
        """Runs Semgrep security scans on the file."""
        specific_rule = self.rule_map.get(file_path.suffix)
        active_rules = [r for r in [specific_rule, self.common_rules] if r and r.exists()]

        for rule_file in active_rules:
            print(f"Scanning: {file_path.name} with {rule_file.name}")
            cmd = ["semgrep", "--config", str(rule_file), "--json", str(file_path)]
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if res.stdout:
                try:
                    data = json.loads(res.stdout)
                    for finding in data.get('results', []):
                        self.results.append({
                            "Timestamp": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                            "File": file_path.name,
                            "Line": finding['start']['line'],
                            "Rule ID": finding['check_id'],
                            "Severity": finding['extra']['severity'],
                            "Message": finding['extra']['message']
                        })
                except Exception:
                    continue

    def export_file_report(self, file_path):
        """Saves findings to Excel, keeping only the latest timestamp and forcing column order."""
        if not self.results:
            return
        
        report_name = f"{file_path.stem}.xlsx"
        new_df = pd.DataFrame(self.results)

        if os.path.exists(report_name):
            existing_df = pd.read_excel(report_name)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            
            # Removes old versions of the same error, keeps the latest timestamp
            final_df = combined_df.drop_duplicates(subset=['File', 'Line', 'Message'], keep='last')
            print(f"🔄 Updated report (Latest timestamp kept): {report_name}")
        else:
            final_df = new_df
            print(f"✨ Created new report: {report_name}")
        
        # FORCE COLUMN ORDER: Ensure 'Timestamp' is always the 1st column
        cols = ['Timestamp'] + [c for c in final_df.columns if c != 'Timestamp']
        final_df = final_df[cols]
        
        final_df.to_excel(report_name, index=False)

    def run(self):
        if not self.target_path.exists():
            print(f"Error: Path {self.target_path} not found.")
            return

        for root, _, files in os.walk(self.target_path):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in self.rule_map:
                    self.results = [] # Reset for each file's individual report
                    self.check_header(file_path)
                    self.review_file(file_path)
                    self.export_file_report(file_path)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    CodeReviewer(args.path).run()