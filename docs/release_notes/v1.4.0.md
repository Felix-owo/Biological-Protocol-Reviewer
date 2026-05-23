# Upgrade Biological-Protocol-Reviewer to v1.4.0

This package is based on the stable v1.3.3 archive and preserves the existing repository layout, tests, schemas, templates, benchmarks, and CI workflow.

## Main changes

- Version updated to `1.4.0`.
- License unified to `MPL-2.0` across `LICENSE`, `SKILL.md`, `pyproject.toml`, and README badges.
- Added `biological-protocol-reviewer/references/agent_behavior_core.md`.
- Added `biological-protocol-reviewer/references/sop_traceability_and_change_discipline.md`.
- Updated `SKILL.md` resource routing to activate the new behavior and SOP-change traceability gates.
- Updated `references/skill_manifest.json` and `scripts/check_installable_skill.py` so the new files are package-integrity requirements.
- Added `tests/test_license_consistency.py`.

## Local upgrade commands

From your local repository root:

```bash
cd ~/Documents/Codex/Biological-Protocol-Reviewer
git status
git checkout main
git pull --ff-only
git checkout -b upgrade-v1.4.0-mpl2
```

Unzip this archive somewhere temporary, then copy the new tree into the repo:

```bash
rsync -av --delete \
  /path/to/Biological-Protocol-Reviewer-1.4.0/ \
  ~/Documents/Codex/Biological-Protocol-Reviewer/
```

Validate:

```bash
python3 -m pytest -q
python3 biological-protocol-reviewer/scripts/check_installable_skill.py --skill-dir biological-protocol-reviewer
python3 biological-protocol-reviewer/scripts/check_version_consistency.py
python3 biological-protocol-reviewer/scripts/run_regression_fixtures.py
python3 tools/score_protocol_benchmark.py --benchmark-root benchmarks/v1.0
```

Review and push:

```bash
git diff --stat
git diff -- LICENSE biological-protocol-reviewer/SKILL.md pyproject.toml
git add .
git commit -m "Upgrade Biological Protocol Reviewer to v1.4.0 and MPL-2.0"
git push -u origin upgrade-v1.4.0-mpl2
```

Then open a pull request into `main`, or merge locally after reviewing the diff.
