#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List

# Color codes for terminal status messages
class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Map extensions to internal language keys
LANGUAGE_MAP = {
    '.js': 'javascript',
    '.jsx': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.py': 'python',
    '.java': 'java',
    '.go': 'go',
}

# Map language keys to your SPECIFIC filenames in the rules/ folder
# Based on your folder structure: common-rules.yml, go-rules.yml, etc.
RULE_FILES = {
    'javascript': ['javascript-rules.yml', 'common-rules.yml'],
    'typescript': ['javascript-rules.yml', 'common-rules.yml'],
    'python': ['python-rules.yml', 'common-rules.yml'],
    'java': ['java-rules.yml', 'common-rules.yml'],
    'go': ['go-rules.yml', 'common-rules.yml'],
}

class CodeReviewer:
    def __init__(self, target_path: str, severity: str = None):
        self.target_path = Path(target_path)
        self.severity = severity
        # Points to the 'rules' folder in your project
        self.rules_dir = Path(__file__).parent / "rules"

    def detect_language(self, file_path: Path) -> str:
        return LANGUAGE_MAP.get(file_path.suffix.lower())

    def get_rule_files(self, language: str) -> List[Path]:
        """Fetches only the rules specific to the detected language"""
        rule_names = RULE_FILES.get(language, [])
        paths = []
        for name in rule_names:
            rule_path = self.rules_dir / name
            if rule_path.exists():
                paths.append(rule_path)
        return paths

    def run_semgrep(self, file_path: Path, rule_files: List[Path]):
        """Runs Semgrep with selected rules and displays native output"""
        cmd = ['semgrep']
        
        for rule_file in rule_files:
            cmd.extend(['--config', str(rule_file)])
        
        if self.severity:
            severities = self.severity.upper().split(',')
            for sev in severities:
                cmd.extend(['--severity', sev.strip()])
        
        cmd.append(str(file_path))

        # Printing a status line before Semgrep takes over the terminal
        print(f"{Colors.BLUE}{Colors.BOLD}🔍 Reviewing {file_path.name} using {len(rule_files)} rule sets...{Colors.END}")
        
        try:
            # Native output is achieved by NOT capturing stdout
            subprocess.run(cmd)
        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.END}")

    def review_file(self, file_path: Path):
        language = self.detect_language(file_path)
        if not language:
            return
        
        rules = self.get_rule_files(language)
        if rules:
            self.run_semgrep(file_path, rules)

    def run(self):
        if self.target_path.is_file():
            self.review_file(self.target_path)
        elif self.target_path.is_dir():
            for ext in LANGUAGE_MAP.keys():
                for file_path in self.target_path.rglob(f"*{ext}"):
                    self.review_file(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='File or directory to review')
    parser.add_argument('--severity', help='e.g. ERROR,WARNING')
    args = parser.parse_args()
    
    CodeReviewer(args.path, args.severity).run()