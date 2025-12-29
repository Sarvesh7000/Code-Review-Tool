import os
import re
import json
import subprocess
import pandas as pd
from pathlib import Path

# --- Constants for Validation ---
SUPPORTED_EXTENSIONS = {
    '.js': 'javascript', '.ts': 'typescript', '.java': 'java',
    '.py': 'python', '.go': 'go'
}

# Fields for Box 1
REQUIRED_HEADER_FIELDS = {
    'Purpose': r'(?i)purpose\s*:',
    'Author': r'(?i)author\s*:',
    'Date Created': r'(?i)date\s*created\s*:',
}

# Fields for Box 2 (Modification Table)
REQUIRED_HISTORY_FIELDS = {
    'Modified by': r'(?i)modified\s+by',
    'Modified Date': r'(?i)modified\s+date',
    'Purpose': r'(?i)purpose',
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
            '.ts': self.rules_dir / 'javascript-rules.yml',
            '.py': self.rules_dir / 'python-rules.yml',
            '.go': self.rules_dir / 'go-rules.yml',
            '.java': self.rules_dir / 'java-rules.yml'
        }

    def extract_comment_blocks(self, file_path):
        """Extracts content based on language: /* */ for C-style, # for Python."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            if file_path.suffix in ['.js', '.ts', '.java', '.go']:
                return re.findall(r'/\*+([\s\S]*?)\*+/', content)
            
            elif file_path.suffix == '.py':
                blocks = re.findall(r'((?:^[ \t]*#.*(?:\n|$))+)', content, flags=re.MULTILINE)
                return [re.sub(r'^[ \t]*#+', '', block, flags=re.MULTILINE) for block in blocks]
            
            return []
        except Exception:
            return []

    def check_header_logic(self, file_path):
        """Validates specific missing fields for both Header and Modification boxes."""
        if file_path.suffix not in SUPPORTED_EXTENSIONS:
            return

        timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_blocks = self.extract_comment_blocks(file_path)

        # --- BOX 1: HEADER COMMENT BOX ---
        header_title_found = False
        if len(comment_blocks) > 0:
            if re.search(r'(?i)HEADER\s+COMMENT\s+BOX', comment_blocks[0]):
                header_title_found = True
                missing_h = [f for f, r in REQUIRED_HEADER_FIELDS.items() if not re.search(r, comment_blocks[0])]
                
                if missing_h:
                    fields_str = ", ".join(missing_h)
                    self.results.append({
                        "Timestamp": timestamp, "File": file_path.name, "Line": 1,
                        "Rule ID": "HEADER-C", "Severity": "ERROR",
                        "Message": f"Missing mandatory field(s): {fields_str} inside Header * comment box"
                    })

        if not header_title_found:
            self.results.append({
                "Timestamp": timestamp, "File": file_path.name, "Line": 1,
                "Rule ID": "HEADER-F", "Severity": "ERROR",
                "Message": "Header * comment box not created"
            })

        # --- BOX 2: MODIFICATION HISTORY ---
        history_block = None
        for block in comment_blocks:
            if re.search(r'(?i)MODIFICATION\s+HISTORY', block):
                history_block = block
                break
        
        if history_block:
            missing_m = [f for f, r in REQUIRED_HISTORY_FIELDS.items() if not re.search(r, history_block)]
            
            if len(missing_m) == 3:
                # All 3 missing
                self.results.append({
                    "Timestamp": timestamp, "File": file_path.name, "Line": 1,
                    "Rule ID": "HEADER-T", "Severity": "ERROR",
                    "Message": "Modification table not created which includes columns as Modified by, Modified Date, Purpose"
                })
            elif missing_m:
                # Specific combination missing
                fields_str = ", ".join(missing_m)
                self.results.append({
                    "Timestamp": timestamp, "File": file_path.name, "Line": 1,
                    "Rule ID": "HEADER-T", "Severity": "ERROR",
                    "Message": f"In Modification table missing columns as {fields_str}"
                })
        else:
            # Block not found at all
            self.results.append({
                "Timestamp": timestamp, "File": file_path.name, "Line": 1,
                "Rule ID": "HEADER-T", "Severity": "ERROR",
                "Message": "Modification table not created which includes columns as Modified by, Modified Date, Purpose"
            })

    def review_file(self, file_path):
        print(f"🔍 Scanning document: {file_path.name}...", end="\r", flush=True)
        specific_rule = self.rule_map.get(file_path.suffix)
        active_configs = []
        if specific_rule and specific_rule.exists():
            active_configs.append(str(specific_rule))
        if self.common_rules.exists():
            active_configs.append(str(self.common_rules))

        for config_path in active_configs:
            cmd = ["semgrep", "--quiet", "--config", config_path, "--json", str(file_path)]
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            if res.stdout.strip():
                try:
                    data = json.loads(res.stdout)
                    for finding in data.get('results', []):
                        self.results.append({
                            "Timestamp": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                            "File": file_path.name, "Line": finding['start']['line'],
                            "Rule ID": finding['check_id'], "Severity": finding['extra']['severity'],
                            "Message": finding['extra']['message']
                        })
                except Exception: pass

    def export_report(self, file_path):
        if not self.results: return
        report_name = f"{file_path.stem}_Review.xlsx"
        report_path = Path(report_name)
        print(" " * 80, end="\r") 
        msg = f"🔄 Updated report : {report_name}" if report_path.exists() else f"✨ Created new report: {report_name}"
        
        df = pd.DataFrame(self.results)
        df['is_header'] = df['Rule ID'].str.contains('HEADER')
        df = df.sort_values(by=['is_header', 'Line'], ascending=[False, True]).drop(columns=['is_header'])

        try:
            df.to_excel(report_name, index=False)
            print(msg)
        except PermissionError:
            alt = f"{file_path.stem}_Review_NEW.xlsx"
            df.to_excel(alt, index=False)
            print(f"⚠️ {report_name} is open. Created {alt} instead.")

    def run(self):
        for root, dirs, files in os.walk(self.target_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'venv']]
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in self.rule_map:
                    self.results = [] 
                    self.check_header_logic(file_path)
                    self.review_file(file_path)
                    self.export_report(file_path)
        print("\n✅ All documents scanned successfully.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to code directory")
    args = parser.parse_args()
    CodeReviewer(args.path).run()
