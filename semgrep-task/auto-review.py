import os
import re
import json
import subprocess
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

SUPPORTED_EXTENSIONS = {
    '.js': 'javascript', '.ts': 'typescript', '.java': 'java',
    '.py': 'python', '.go': 'go'
}

REQUIRED_HEADER_FIELDS = {
    'Purpose': r'(?i)purpose\s*:',
    'Author': r'(?i)author\s*:',
    'Date Created': r'(?i)date\s*created\s*:',
}

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
        self.cached_findings = {} # Store pre-scanned Semgrep findings
        
        self.rule_map = {
            '.js': self.rules_dir / 'javascript-rules.yml',
            '.ts': self.rules_dir / 'javascript-rules.yml',
            '.py': self.rules_dir / 'python-rules.yml',
            '.go': self.rules_dir / 'go-rules.yml',
            '.java': self.rules_dir / 'java-rules.yml'
        }

    def pre_scan_semgrep(self):
        """Optimized: Runs Semgrep on the whole folder once per rule file."""
        print("🚀 Initializing security engine... Please wait.", flush=True)
        
        configs_to_run = set()
        if self.common_rules.exists():
            configs_to_run.add(str(self.common_rules))
        for r_path in self.rule_map.values():
            if r_path.exists():
                configs_to_run.add(str(r_path))

        for config in configs_to_run:
            cmd = ["semgrep", "scan", "--quiet", "--config", config, "--json", str(self.target_path)]
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            if res.stdout.strip():
                try:
                    data = json.loads(res.stdout)
                    for finding in data.get('results', []):
                        fname = Path(finding['path']).name
                        if fname not in self.cached_findings:
                            self.cached_findings[fname] = []
                        
                        self.cached_findings[fname].append({
                            "Timestamp": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                            "File": fname, "Line": finding['start']['line'],
                            "Rule ID": finding['check_id'], "Severity": finding['extra']['severity'],
                            "Message": finding['extra']['message']
                        })
                except Exception:
                    pass

    def extract_comment_blocks(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            blocks_with_lines = []
            if file_path.suffix in ['.js', '.ts', '.java', '.go']:
                for match in re.finditer(r'/\*+([\s\S]*?)\*+/', content):
                    start_line = content.count('\n', 0, match.start()) + 1
                    blocks_with_lines.append((match.group(1), start_line))
                return blocks_with_lines
            elif file_path.suffix == '.py':
                for match in re.finditer(r'((?:^[ \t]*#.*(?:\n|$))+)', content, flags=re.MULTILINE):
                    start_line = content.count('\n', 0, match.start()) + 1
                    clean_block = re.sub(r'^[ \t]*#+', '', match.group(1), flags=re.MULTILINE).strip()
                    blocks_with_lines.append((clean_block, start_line))
                return blocks_with_lines
            return []
        except Exception:
            return []

    def check_header_logic(self, file_path): 
        if file_path.suffix not in SUPPORTED_EXTENSIONS:
            return

        timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_blocks = self.extract_comment_blocks(file_path)
        actual_mod_dt = datetime.fromtimestamp(os.path.getmtime(file_path)).replace(second=0, microsecond=0)

        header_box_found = False
        vc_table_found = False

        for block, block_start_line in comment_blocks:
            if re.search(r'(?i)HEADER\s+COMMENT\s+BOX', block):
                header_box_found = True
                for field, pattern in REQUIRED_HEADER_FIELDS.items():
                    if not re.search(pattern, block):
                        self.results.append({
                            "Timestamp": timestamp, "File": file_path.name, "Line": block_start_line,
                            "Rule ID": "HEADER-FIELD", "Severity": "ERROR", 
                            "Message": f"Header Comment Box is missing required field: '{field}'"
                        })

            if re.search(r'(?i)VERSION\s+CONTROL\s+TABLE', block):
                vc_table_found = True
                for field, pattern in REQUIRED_HISTORY_FIELDS.items():
                    if not re.search(pattern, block):
                        self.results.append({
                            "Timestamp": timestamp, "File": file_path.name, "Line": block_start_line,
                            "Rule ID": "VCT-COLUMN", "Severity": "ERROR", 
                            "Message": f"Version Control Table is missing column: '{field}'"
                        })

                raw_lines = block.split('\n')
                all_found_dts = [] 
                for i, line in enumerate(raw_lines):
                    current_line_no = block_start_line + i
                    stripped_line = line.strip()
                    if not stripped_line or re.match(r'^\*+\s*/?$', stripped_line): continue
                    if "VERSION CONTROL" in stripped_line.upper(): continue
                    
                    if "---" in stripped_line:
                        if len(re.findall(r'-{3,}', stripped_line)) < 3 or stripped_line.count("|") < 4:
                            self.results.append({
                                "Timestamp": timestamp, "File": file_path.name, "Line": current_line_no,
                                "Rule ID": "HEADER-T-FMT", "Severity": "ERROR", 
                                "Message": f"Version Control Table formatting error: Row {current_line_no} has invalid separator format ('---')"
                            })
                    elif stripped_line.count("|") > 0 and stripped_line.count("|") < 4:
                        self.results.append({
                            "Timestamp": timestamp, "File": file_path.name, "Line": current_line_no,
                            "Rule ID": "HEADER-T-FMT", "Severity": "ERROR", 
                            "Message": f"Version Control Table formatting error: Row {current_line_no} missing separators ('|')"
                        })
                    
                    found_dt_strs = re.findall(r'(\d{2,4}-\d{2}-\d{2,4}\s+\d{1,2}:\d{2}\s?[apAP][mM]?)', stripped_line)
                    if not found_dt_strs:
                        found_dt_strs = re.findall(r'(\d{2,4}-\d{2}-\d{2,4})', stripped_line)

                    for dt_str in found_dt_strs:
                        fmts = ["%d-%m-%Y %I:%M%p", "%d-%m-%Y %I:%M %p", "%Y-%m-%d %I:%M%p", "%Y-%m-%d %I:%M %p", 
                                "%d-%m-%Y %H:%M", "%Y-%m-%d %H:%M", "%d-%m-%Y", "%Y-%m-%d"]
                        for fmt in fmts:
                            try:
                                parsed_dt = datetime.strptime(dt_str.strip(), fmt)
                                all_found_dts.append((parsed_dt, current_line_no, dt_str))
                                break
                            except ValueError: continue

                if all_found_dts:
                    latest_entry = max(all_found_dts, key=lambda x: x[0])
                    latest_dt, latest_line, latest_str = latest_entry
                    time_diff_mins = abs((actual_mod_dt - latest_dt).total_seconds() / 60)
                    if time_diff_mins > 5:
                        self.results.append({
                            "Timestamp": timestamp, "File": file_path.name, "Line": latest_line,
                            "Rule ID": "HEADER-D", "Severity": "ERROR",
                            "Message": f"In Version Control Table, the latest Modified Date/Time (Found: {latest_str}) "
                                       f"does not match actual Modified date file (Actual: {actual_mod_dt.strftime('%Y-%m-%d %I:%M %p')})."
                        })

        if not header_box_found:
            self.results.append({"Timestamp": timestamp, "File": file_path.name, "Line": 1, "Rule ID": "HEADER-BOX-MISSING", "Severity": "ERROR", "Message": "Header Comment Box not found in file."})
        if not vc_table_found:
            self.results.append({"Timestamp": timestamp, "File": file_path.name, "Line": 1, "Rule ID": "HEADER-T-MISSING", "Severity": "ERROR", "Message": "Version Control Table not found in file."})

    def review_file_fast(self, file_path):
        """Pulls findings from memory cache instead of running a subprocess."""
        print(f"🔍 Scanning document: {file_path.name}...", end="\r", flush=True)
        findings = self.cached_findings.get(file_path.name, [])
        self.results.extend(findings)

    def export_report(self, file_path):
        if not self.results: return
        report_name = f"{file_path.stem}_Review.xlsx"
        report_path = Path(report_name)
        is_update = report_path.exists()
        
        df = pd.DataFrame(self.results)
        df['is_header'] = df['Rule ID'].str.contains('HEADER|VCT')
        df = df.sort_values(by=['is_header', 'Line'], ascending=[False, True]).drop(columns=['is_header'])
        
        try:
            df.to_excel(report_name, index=False)
            print(" " * 80, end="\r") 
            if is_update:
                print(f"🔄 Updated report : {report_name}")
            else:
                print(f"✨ Created new report: {report_name}")
        except PermissionError:
            updated_report_name = f"{file_path.stem}_Review_updated.xlsx"
            df.to_excel(updated_report_name, index=False)
            print(" " * 80, end="\r") 
            print(f"⚠️ {report_name} is opened. So created another file named {updated_report_name}")

    def run(self):
        # STEP 1: Fast scan everything at once (The Speed Boost)
        self.pre_scan_semgrep()
        
        # STEP 2: Process files one by one with original messages
        for root, dirs, files in os.walk(self.target_path):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'venv', '__pycache__']]
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in self.rule_map:
                    self.results = [] 
                    self.check_header_logic(file_path) # Fast Python logic
                    self.review_file_fast(file_path)  # Instant cache lookup
                    self.export_report(file_path)     # Original display messages
        print("\n✅ All documents scanned successfully.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to code directory")
    args = parser.parse_args()
    CodeReviewer(args.path).run()