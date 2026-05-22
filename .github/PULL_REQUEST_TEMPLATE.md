## Summary

- 

## Validation

- [ ] `python biological-protocol-reviewer/scripts/check_installable_skill.py --skill-dir biological-protocol-reviewer`
- [ ] `python biological-protocol-reviewer/scripts/check_version_consistency.py`
- [ ] `python biological-protocol-reviewer/scripts/run_regression_fixtures.py`
- [ ] `python -m unittest discover -s tests -v`
- [ ] `python tools/score_protocol_benchmark.py --benchmark-root benchmarks/v1.0`

## Skill Package Check

- [ ] No repository-root docs were added inside `biological-protocol-reviewer/`.
- [ ] New runtime resources are referenced from `SKILL.md`.
- [ ] Version strings and templates are consistent.
- [ ] No private protocols, unpublished data, local paths, or credentials are included.
