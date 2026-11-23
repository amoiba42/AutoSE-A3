# Seeded PRs

Five hand-made pull requests. Each has a known correct verdict. Used in D8 (reviewer independence).

Written by hand, not by AutoSE. Each passes the existing test suite (except the one upstream collection error every commit has). So the reviewer must read the code to find the planted bug.

## Files

| Path | What it is |
|---|---|
| `sN.diff` | The change, against the base branch |
| `notes/sN.md` | Design and attempt summary. Shown to the reviewer in the "notes" variant only |
| `notes/prN.md` | Same, for real AutoSE PRs #7–#9 |

The reviewer never sees this folder, the labels below, or the PR body.

## Seeds

Branches: `seeded/s1` … `seeded/s5` on the test fork (draft PRs).

| Seed | PR | Issue | Expected | Planted defect |
|---|---|---|---|---|
| S1 | [#10](https://github.com/amoiba42/markdown/pull/10) | #5 wikilink label | approve | none |
| S2 | [#11](https://github.com/amoiba42/markdown/pull/11) | #5 wikilink label | changes_requested | Href built from the label: `[[Target\|Label]]` links to `/Label/`. Only test checks the text |
| S3 | [#12](https://github.com/amoiba42/markdown/pull/12) | #4 scheme autolinks | changes_requested | Test is weak: asserts `"tel" in output`, which passes without the change. No code-span test |
| S4 | [#13](https://github.com/amoiba42/markdown/pull/13) | #4 scheme autolinks | approve | none |
| S5 | [#14](https://github.com/amoiba42/markdown/pull/14) | #4 scheme autolinks | changes_requested | Priority 105 is below automail (110), so `<skype:user@example.com>` becomes `mailto:` |

Summary: 2 clean (S1, S4), 3 defective (S2 code, S3 test, S5 code).

## Check

On 2026-11-22: all seeds pass the existing suite. S3 and S4 pass the hidden tests for fork issue #4 (`hidden_tests/test_issue3_autolink.py`).
