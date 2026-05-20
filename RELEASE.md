# Release Notes

## Current Release: v1.1.2

`v1.1.2` is a Markdown-first SOP release. It changes the default revised
protocol output to `Revised_Protocol.md` and removes DOCX rendering from the
default workflow.

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

- The revised protocol is emitted as Markdown by default: `Revised_Protocol.md`.
- Codex should install only the `Biological-Protocol-Reviewer/` subdirectory.
- The validator uses `--protocol Revised_Protocol.md` rather than DOCX parsing.
