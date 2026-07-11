# Contributing

This repository contains one installable Agent Skill package:
`biological-protocol-reviewer/`.

Keep GitHub-facing documentation, release notes, CI, and tests at the repository
root. Keep only runtime skill resources inside `biological-protocol-reviewer/`.

Before opening a pull request, run:

```bash
python biological-protocol-reviewer/scripts/check_installable_skill.py --skill-dir biological-protocol-reviewer
python biological-protocol-reviewer/scripts/check_version_consistency.py --mode release --repo-root .
python biological-protocol-reviewer/scripts/run_regression_fixtures.py
python -m unittest discover -s tests -v
python tools/score_protocol_benchmark.py --benchmark-root benchmarks/v1.0
```

Do not commit private protocols, unpublished data, local paths, credentials,
copyrighted full-text papers, or institution-specific approvals.
