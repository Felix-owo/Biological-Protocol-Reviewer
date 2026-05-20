# Release Notes

## Current Release: v1.1.1

`v1.1.1` is a packaging and document-style release. It keeps the installable
Codex skill isolated in `Biological-Protocol-Reviewer/` while leaving GitHub
repository documentation at the root.

### Installable Skill Path

```text
Biological-Protocol-Reviewer/
```

### Validation Before Release

```bash
test -f Biological-Protocol-Reviewer/SKILL.md
test ! -f SKILL.md
env PYTHONPYCACHEPREFIX=/private/tmp/codex_pycache python3 -m py_compile Biological-Protocol-Reviewer/scripts/protocol_output_validator.py
python3 Biological-Protocol-Reviewer/scripts/protocol_output_validator.py --help
```

### Release Scope

- Repository root is now for README, license, changelog, and release material.
- Codex should install only the `Biological-Protocol-Reviewer/` subdirectory.
- Heading style guidance now uses `Smiley Sans` / `得意黑` without extra bold.
