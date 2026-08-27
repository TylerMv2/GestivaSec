"""
Gestiva Security (GestivaSec V1) — YARA Pattern Scanning Infrastructure Component
Scans payload snippets and log text artifacts for known threat signature patterns.
"""
import re
from typing import List, Dict, Any, Optional
from backend.domain.threat_intel_engine import YaraMatchResult

_YARA_PATTERNS = [
    {
        "rule_name": "YARA_REVERSE_SHELL_PAYLOAD",
        "regex": r"(?:/bin/bash\s+-i|nc\s+-e\s+/bin/sh|powershell\s+-nop\s+-w\s+hidden\s+-e)",
        "severity": "CRITICAL",
        "description": "Reverse shell payload execution string detected."
    },
    {
        "rule_name": "YARA_MIMIKATZ_LSASS_DUMP",
        "regex": r"(?:sekurlsa::logonpasswords|lsass\.dmp|lsadump::sam)",
        "severity": "CRITICAL",
        "description": "Mimikatz LSASS credential dumping command detected."
    },
    {
        "rule_name": "YARA_WEBSHELL_EVAL_BASE64",
        "regex": r"(?:eval\(base64_decode\(|passthru\(|system\(\$_POST)",
        "severity": "HIGH",
        "description": "PHP WebShell command execution pattern detected."
    }
]

class YaraScannerService:
    def scan_content(self, content: str) -> List[YaraMatchResult]:
        """Scans arbitrary text or payload snippet against YARA rule patterns."""
        matches = []
        if not content:
            return matches

        for rule in _YARA_PATTERNS:
            found = re.findall(rule["regex"], content, re.IGNORECASE)
            if found:
                matches.append(
                    YaraMatchResult(
                        rule_name=rule["rule_name"],
                        matched_strings=list(set(found)),
                        severity=rule["severity"],
                        description=rule["description"]
                    )
                )

        return matches
