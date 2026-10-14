"""Adversarial GTS v0.1 manifest tests."""
import copy
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("gts_verifier", Path(__file__).resolve().parents[1] / "scripts" / "verify_manifest.py")
gts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gts)


def good():
    return {
        "gts_version": "0.1",
        "subject": {"repository": "example/repo", "commit": "a" * 40, "artifact_digest": "sha256:" + "b" * 64},
        "checks": {name: {"status": "pass", "evidence": "urn:example:" + name, "scope": "test", "verifier": "test-observer"} for name in gts.REQUIRED},
        "decision": "PASS",
    }


class ReleaseGateTests(unittest.TestCase):
    def test_complete_manifest_is_only_completeness_pass(self):
        self.assertEqual(gts.assess(good())[0], "PASS")

    def test_all_missing_checks_hold(self):
        for name in gts.REQUIRED:
            with self.subTest(name=name):
                item = good()
                del item["checks"][name]
                item["decision"] = "HOLD"
                self.assertEqual(gts.assess(item)[0], "HOLD")

    def test_denial_failure_and_skips(self):
        for status, decision in [("fail", "FAIL"), ("hold", "HOLD"), ("skip", "HOLD")]:
            with self.subTest(status=status):
                item = good()
                item["checks"]["wiring"]["status"] = status
                item["decision"] = decision
                verdict, problems = gts.assess(item)
                self.assertEqual(verdict, decision)
                self.assertFalse(any("disagrees with computed" in p for p in problems), problems)

    def test_missing_evidence_never_passes(self):
        for key in ("evidence", "scope", "verifier"):
            item = good()
            item["checks"]["observation"][key] = ""
            item["decision"] = "HOLD"
            self.assertEqual(gts.assess(item)[0], "HOLD")

    def test_false_pass_is_rejected(self):
        item = good()
        item["checks"]["authority"]["status"] = "skip"
        self.assertEqual(gts.assess(item)[0], "FAIL")

    def test_malformed_inputs_fail(self):
        for change in [
            lambda d: d.update(gts_version="other"),
            lambda d: d["subject"].update(commit="HEAD"),
            lambda d: d["subject"].update(artifact_digest="unsigned"),
            lambda d: d["checks"].update(extra={"status": "pass"}),
            lambda d: d["checks"]["authority"].update(status="green"),
            lambda d: d["checks"]["authority"].update(status=[]),
        ]:
            item = good()
            change(item)
            self.assertEqual(gts.assess(item)[0], "FAIL")


if __name__ == "__main__":
    unittest.main()
