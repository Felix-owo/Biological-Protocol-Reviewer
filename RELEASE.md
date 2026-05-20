# Release Notes

## Current Release: v1.1.3

`v1.1.3` is a repository hardening release. It removes a redundant legacy
reference, cleans local validation paths from release docs, and tightens
frontier-method safety limits while keeping the Markdown-first SOP workflow.

### Installable Skill Path

```text
Biological-Protocol-Reviewer/
```

### Validation Before Release

```bash
test -f Biological-Protocol-Reviewer/SKILL.md
test ! -f SKILL.md
env PYTHONPYCACHEPREFIX=.pycache-check python3 -m py_compile Biological-Protocol-Reviewer/scripts/protocol_output_validator.py
python3 Biological-Protocol-Reviewer/scripts/protocol_output_validator.py --help
```

### Release Scope

- The revised protocol is emitted as Markdown by default: `Revised_Protocol.md`.
- Codex should install only the `Biological-Protocol-Reviewer/` subdirectory.
- The validator uses `--protocol Revised_Protocol.md` rather than DOCX parsing.
- Legacy unreferenced SOP rewrite guidance was removed from the installable
  skill.
- Frontier modules now explicitly avoid parameter optimization that would
  enhance harmful delivery or containment evasion.
