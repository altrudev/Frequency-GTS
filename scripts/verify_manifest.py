#!/usr/bin/env python3
"""GTS v0.1 manifest-completeness checker (not evidence verification)."""
import json
import re
import sys
from pathlib import Path

REQUIRED = frozenset({
    "authority", "execution", "observation", "adversarial",
    "wiring", "provenance", "rollback", "independent_review",
})
SHA = re.compile(r"^[0-9a-fA-F]{40}$")
DIGEST = re.compile(r"^sha256:[0-9a-fA-F]{64}$")


def assess(data):
    if not isinstance(data, dict) or data.get("gts_version") != "0.1":
        return "FAIL", ["invalid GTS version or manifest"]
    subject = data.get("subject")
    if not isinstance(subject, dict) or not isinstance(subject.get("repository"), str) or not subject["repository"].strip() or not isinstance(subject.get("commit"), str) or not SHA.fullmatch(subject["commit"]) or not isinstance(subject.get("artifact_digest"), str) or not DIGEST.fullmatch(subject["artifact_digest"]):
        return "FAIL", ["invalid or unpinned subject"]
    checks = data.get("checks")
    if not isinstance(checks, dict):
        return "FAIL", ["checks must be a keyed object"]
    problems = []
    failed = False
    for name in sorted(REQUIRED):
        item = checks.get(name)
        if not isinstance(item, dict):
            problems.append(f"{name}: absent")
            continue
        status = item.get("status")
        if status not in ("pass", "fail", "hold", "skip"):
            problems.append(f"{name}: invalid status")
            failed = True
            continue
        if status == "fail":
            failed = True
            problems.append(f"{name}: fail")
        elif status != "pass":
            problems.append(f"{name}: {status}")
        for field in ("evidence", "scope", "verifier"):
            value = item.get(field)
            if not isinstance(value, str) or not value.strip():
                problems.append(f"{name}: missing {field}")
    unexpected = set(checks).difference(REQUIRED)
    if unexpected:
        problems.append("unexpected checks: " + ", ".join(sorted(unexpected)))
        failed = True
    verdict = "FAIL" if failed else ("HOLD" if problems else "PASS")
    declared = data.get("decision")
    if declared not in ("PASS", "HOLD", "FAIL") or declared != verdict:
        problems.append(f"declared decision {declared!r} disagrees with computed {verdict}")
        return "FAIL", problems
    return verdict, problems


def main(argv=None):
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print("usage: verify_manifest.py manifest.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"FAIL: cannot read manifest: {exc}", file=sys.stderr)
        return 1
    verdict, problems = assess(data)
    print(verdict + (": " + "; ".join(problems) if problems else ": manifest complete; evidence NOT authenticated"))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
