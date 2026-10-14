# Governance Testing Standard (GTS) — evidence-driven release contract

**Status:** Draft v0.1. Not a certification, third-party endorsement, or claim that Frequency has passed.

GTS is a technology-neutral minimum evidence contract for consequential software changes. Its release decisions are `PASS`, `HOLD`, and `FAIL`. Unknown, missing, skipped, not-applicable without justification, and unexecuted checks **never** become a pass.

## Required release evidence

A release manifest uses `gts-version: "0.1"` (JSON field `gts_version`) and records:

- `subject`: repository, immutable full commit SHA, artifact digest (SHA-256)
- `checks`: independently addressable entries for `authority`, `execution`, `observation`, `adversarial`, `wiring`, `provenance`, `rollback`, and `independent_review`
- Each entry: `status` (`pass`, `fail`, `hold`, `skip`), `evidence` (nonempty durable reference), `scope`, and `verifier`
- `decision`: stated expected result, **not** an override of the computed verdict

Each PASS needs a concrete evidence locator, a named verifier, and a scope. A reference alone is a *claim requiring examination*: the checker only validates manifest completeness and consistency, **not** the authenticity, independence, or correctness of referenced evidence. A release is not independently verified merely because the manifest passes schema checks.

## Normative release invariants

1. Any required check missing, marked HOLD/SKIP, or lacking evidence implies HOLD.
2. Any required check explicitly failing implies FAIL.
3. Only eight passing mandatory checks with complete metadata permit a **manifest-completeness PASS**. A separate human/release authority must still validate evidence and authorize production release.
4. Test counts, adapter registrations, code-review comments, signed attestations, and dispatch receipts are never substituted for observed outcomes.
5. The verifier must refuse contradictory claims such as `decision=PASS` when computed result is HOLD/FAIL.
6. Intent, delegated authority, dispatch, execution, observation, outcome, proof, and promotion are different claims.
7. An observer that merely repeats a producer's assertion does not establish independence.
8. All evidence and check records must reference the same immutable subject version; source or artifact changes invalidate prior release acceptance.
9. Adversarial coverage must include denial/bypass, stale authority, tampering, failures, and required wiring, with explicit environment limits.
10. Any override to a release gate is an independently authorized, auditable exception; an exception is never silently turned into a PASS.

## Executable contract

Run `python3 scripts/verify_manifest.py path/to/manifest.json`; exit 0 for manifest-completeness PASS, exit 1 for HOLD/FAIL or invalid inputs. Run `python3 -m unittest discover -s tests -v` to exercise positive, missing-gate, denied, and inconsistent-decision cases. Neither operation proves live runtime enforcement.

**Implementation scope:** This public specification and its checker are separate from the proprietary Frequency runtime. Frequency must explicitly adopt this contract and generate real evidence before claiming conformance.

Copyright © 2026 Valentyn Rukhaylo / Altru.dev. Apache-2.0; see LICENSE.
