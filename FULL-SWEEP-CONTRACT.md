# Mandatory DDC/Frequency full-sweep contract

When an operator requests a **full sweep**, execution MUST run through the applicable DDC/Frequency assurance path. A standalone unit-test run, lint pass, manual review, or claimed sweep is not equivalent. This contract applies to all Altru/DDC/Frequency projects and third-party contributions assessed through Frequency.

## Required gates

1. **Scope and baseline:** pin repository, exact commit, worktree, dependencies, environment, acceptance claims, and authority limits; identify the DDC/Frequency execution and observation path.
2. **Structural and policy review:** inspect trust boundaries, authorization, data flows, privacy/IP, dependency and supply-chain risks, failure/recovery paths, durable state, and cross-component composition.
3. **Positive and negative controls:** prove valid permitted behavior and rejection of invalid or unauthorized behavior.
4. **Adversarial tests (mandatory):** exercise malformed and type-confused inputs, substitution, replay, tampering, stale/revoked authority, bypass attempts, missing or contradictory evidence, ordering/race/retry/restart ambiguity, and unintended disclosure where applicable. Record inapplicable scenarios with reasons, never silently omit them.
5. **Mutation and regression:** weaken or remove each safety-critical guard in a controlled test and demonstrate a detecting failure; run affected regressions and the applicable complete test/build/lint/conformance suites. Where mutation is unsafe or technically unavailable, report the untested gate as a limitation.
6. **Independent observation and evidence:** distinguish declarations, dispatch, execution, effects, and externally observed results. Preserve exact revision, commands, outcomes, logs, artifacts, and durable receipts; independently verify material claims wherever possible.
7. **Closure:** recheck changes, unresolved findings, scope drift, secrets, and evidence integrity. Explicitly classify results as PASS, FAIL, BLOCKED, or NOT_APPLICABLE with rationale. A mandatory gate that is failed, blocked, or unverified prevents a claim of completed full sweep.

## Reporting and promotion

Report the exact revision and environment, DDC/Frequency path used, adversarial matrix, test counts, observed failures and repairs, unverified boundaries, and artifact/receipt references. Use the lifecycle **constructed → internally tested → adversarially tested → independently observed → acceptance verified → regressions checked → evidence closed → releasable**. Never conflate synthetic tests with live-peer, hardware, or production assurance. No merge or deployment claim follows solely from passing tests.
