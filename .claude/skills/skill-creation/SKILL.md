---
name: skill-creation
description: Guide for creating new Claude Code skills for this audit project
disable-model-invocation: true
---

# Creating New Skills

## Skill Structure

Each skill lives in `.claude/skills/<skill-name>/` and must contain a `SKILL.md` file.

```
.claude/skills/<skill-name>/
├── SKILL.md          # Required - skill definition
├── scripts/          # Optional - Python utilities
│   └── tool.py
└── SUPPORTING.md     # Optional - large templates/reference
```

## SKILL.md Frontmatter (Required)

```yaml
---
name: short-command-name        # Used as /command (e.g., /awp)
description: One-line summary   # Shown in skill listings
disable-model-invocation: true  # Optional - user-only via slash command
---
```

## Rules

1. **Name**: lowercase, hyphenated (e.g., `audit-working-papers`)
2. **SKILL.md**: Keep focused. One skill = one capability area
3. **Scripts**: Place Python utilities in `scripts/` subfolder
4. **Templates**: If a template is large (>50 lines), put it in a separate `.md` file
5. **No client data**: Skills are generic frameworks, never client-specific

## This Project's Conventions

- Skills map to audit workflow phases
- Python scripts use `openpyxl` for Excel, `python-docx` for Word
- Output always goes to `Clients/` directory
- Every engagement needs an HTML viewer (see `/viewer` skill)

## Checklist

- [ ] `SKILL.md` has YAML frontmatter with `name` and `description`
- [ ] Content is self-contained (doesn't depend on CLAUDE.md details)
- [ ] If scripts exist, they're in `scripts/` subfolder
- [ ] Skill is referenced in CLAUDE.md skills table
- [ ] No client-specific data included
