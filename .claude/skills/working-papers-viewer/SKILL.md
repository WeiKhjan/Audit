---
name: viewer
description: Generate interactive HTML viewer and START_VIEWER.bat for audit working papers
---

# Working Papers Viewer

## Requirement

**EVERY engagement MUST have:**
1. `audit_viewer.html` - Interactive HTML viewer for all working papers
2. `START_VIEWER.bat` - Batch file to launch the viewer

## When to Generate

| Trigger | Action |
|---------|--------|
| New working paper created | Add to sections array, regenerate HTML |
| Working paper deleted | Remove from sections array, regenerate HTML |
| New section/folder added | Add new section object, regenerate HTML |
| Content updated only | No HTML change needed (auto-loads) |
| Final submission | Full regeneration and QC check |

## START_VIEWER.bat Template

See `VIEWER_TEMPLATE.md` in this skill folder for the full HTML and BAT templates.

The batch file must:
- Display client name, company number, FYE in ASCII banner
- Start Python HTTP server on port 8888
- Auto-open browser after 2 seconds
- Fall back to python3 if python fails

## audit_viewer.html Requirements

### Structure
1. **Header** - Client name, company no, FYE, framework, status badge
2. **Nav Panel (Left)** - Search box, collapsible sections (A-G), file items, Download All button
3. **Preview Panel (Right)** - Breadcrumb, document title, rendered markdown

### Required JS Functions
- `loadFile(folder, filename, displayName, ref)` - Load and render markdown
- `searchFiles(query)` - Filter navigation items
- `downloadAllDocuments()` - Generate offline HTML with all documents

### Download All Feature (CRITICAL)
Must: fetch all markdown files, convert via marked.js, create standalone HTML with inline CSS, properly escape script tags (`'<scr' + 'ipt>'`), store content in hidden divs, work completely offline.

### CSS Styling
- Nav panel: dark theme (#1e293b)
- Preview: white background
- Accents: blue (#60a5fa, #3b82f6)
- Tables: header gradient, alternating rows, hover highlight
- Query badges: red (#fef2f2 bg, #dc2626 text)
- Responsive resizer between panels

## Reference

See `Clients/AWP_Guoan_Cable_FYE2025/audit_viewer.html` for working example.
