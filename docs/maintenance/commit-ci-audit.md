# Commit CI Audit Ledger

Persistent repository-specific record of commit-level CI checks and red-cross investigations.

## How to use this ledger

1. Read this file before auditing commit checks.
2. Check only commits newer than the checkpoint, plus older **red**, **pending**, or explicitly unresolved entries.
3. Record exact commit SHAs and observed results; never infer from missing badges or empty API responses.
4. Preserve failures and append diagnosis, fix, rerun, and final-outcome evidence.
5. Advance the checkpoint only after reviewing the range; carry unresolved entries forward.

## Result meanings

| Result | Meaning |
|---|---|
| **green** | Completed successful check/run directly observed. |
| **red** | Completed failing check/run directly observed. |
| **pending** | Check/run exists but is unfinished. |
| **unavailable** | Available evidence did not expose a result; not a pass or failure. |
| **not applicable** | Workflow configuration confirms no relevant check is triggered. |

## Checkpoint

- Repository: `SakibShahariar/material-gnome-theme`
- Default branch: `master`
- Checkpoint SHA: `c4f7af5e60300336fa89519ba254a64fbdf2b546`
- Initialized: 2026-11-02
- Baseline: latest branch tip queried through combined commit-status endpoint; empty status list recorded as **unavailable**, not green/red. Older history was not retroactively audited during setup.
- Next session: review commits after this checkpoint, including the ledger and `AGENTS.md` setup commits; investigate any older red/pending commit specifically identified by the owner.

## Initial baseline

| Commit SHA | Subject | CI result | Checked | Follow-up |
|---|---|---|---|---|
| `a1df06eb0fbb9cbcff6423606a0ff00a1e48d3ae` | Default-branch tip at ledger initialization | unavailable | 2026-11-02 | Combined status lookup returned no entries. Revisit if new run or visible failure evidence appears. |

## Red-cross investigation log

### 2026-11-24 — layout-template placeholder regression

- Commit SHAs: `ca76a7b`, `d7166c1`, `f5feb33`, `a82b9ce`, `f8212d0`, `c4f7af5` (and later commits on the same branch)
- Workflow / run: CI `validate` — e.g. https://github.com/SakibShahariar/material-gnome-theme/actions/runs/45360452216/job/138328875831
- Failed job / step: `validate` → "Validate theme assets and stylesheets"
- Failure summary: `check-theme.py` reported unexpanded `{{...}}` placeholders in all 14 files under `gnome-shell/layout-templates/`; `theme-doctor.py` had the same rule.
- Classification: regression introduced by `ca76a7b` (new matugen-variable layout templates) because the placeholder check skipped only files whose *name* contains "template", not files inside a template directory.
- Fix: skip CSS files under any path whose parent directory contains "template" in both `scripts/check-theme.py` and `scripts/theme-doctor.py` (this commit).
- Verification: full CI sequence reproduced locally — `check-theme.py` pass, 620 preset `--dry-run` runs pass, `theme-doctor.py` 5 passed / 0 failed, `bash -n install.sh` pass, isolated-home installer and release-ZIP layout pass.
- Rerun result: pending CI confirmation on the fix commit.

### Historical failures (resolved)

- Commits such as `9975ea9f`, `8e12ce09`, `90f0009f` failed the `validate` job with preset-schema errors (`_meta.variant` mismatch, missing `shade-color` token) during the Matugen preset regeneration. These are pre-existing failures from intermediate work, not regressions from the 2026-11-24 changes; current `check-theme.py` reports 500/500 curated presets valid.

### Failure record template

- Commit SHA:
- Commit subject:
- First observed (date):
- Workflow / run URL:
- Failed job / step:
- Failure summary:
- Classification: regression / pre-existing / inconclusive
- Fix commit(s):
- Rerun attempt(s) and result:
- Final verified outcome:
- Remaining follow-up:

## Session history

| Date | Reviewed range / checkpoint | Result summary |
|---|---|---|
| 2026-11-02 | Initial checkpoint: `a1df06eb0fbb9cbcff6423606a0ff00a1e48d3ae` | Latest commit queried; empty status response recorded as unavailable. Earlier history not retroactively audited. |
| 2026-11-24 | `a1df06e..c4f7af5` (421 commits) | 31 red, 444 green, rest unavailable. Current reds traced to layout-template placeholders; validator fix in this commit; historical presets-schema reds resolved. |
