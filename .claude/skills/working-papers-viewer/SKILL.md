---
name: viewer
description: Generate interactive HTML viewer, server, and START_VIEWER.bat for audit working papers
---

# Working Papers Viewer

## Requirement

**EVERY engagement MUST have these 4 files:**
1. `audit_viewer.html` - Interactive HTML viewer with full feature set
2. `server.py` - Python local server with API endpoints
3. `START_VIEWER.bat` - Batch file to launch the viewer
4. `master_data.json` - Shared variable data for the engagement

## When to Generate

| Trigger | Action |
|---------|--------|
| New engagement created | Generate all 4 files from templates |
| New working paper created | Add to sections array in HTML, regenerate |
| Working paper deleted | Remove from sections array, regenerate |
| New section/folder added | Add new section object, regenerate |
| Content updated only | No regeneration needed (auto-loads via server) |
| Final submission | Full regeneration and QC check |

## File Templates

All templates are in `VIEWER_TEMPLATE.md` in this skill folder. The template contains:

1. **`server.py`** - Python server with endpoints:
   - `GET /api/master` - Read master_data.json
   - `PUT /api/master` - Save master data with timestamp
   - `PUT /api/save` - Save edited markdown files
   - `PUT /api/upload` - Upload .docx/.pdf files (base64 encoded)
   - `GET /api/attachments` - List all .docx/.pdf files across section folders
   - `POST /api/chat` - Proxy to Anthropic API (tool-use support)
   - `GET /api/files` - List all markdown files
   - `GET /api/skills` / `GET /api/skills/{id}` - Read skill documents
   - No-cache headers on all responses
   - ThreadingHTTPServer on port 8000

2. **`START_VIEWER.bat`** - Batch launcher:
   - Display: Company name, company number, FYE, reporting framework
   - Deliverables list: Sections A-G
   - Runs `python server.py` on port 8000
   - Auto-opens browser to `audit_viewer.html`

3. **`audit_viewer.html`** - Full-featured viewer (~3000 lines):
   - Variable system (`{{variable_name}}` with modifiers)
   - Inline variable editing (click-to-edit popovers)
   - Master data editor (full-page, tab-based)
   - File navigation with collapsible A-G sections
   - Edit mode (Toast UI WYSIWYG editor)
   - Sign-off system (preparer + reviewer)
   - Review notes (text selection → highlight → modal)
   - Cross-file review summary
   - Bulk sign-off
   - Download All (standalone offline HTML)
   - AI chat agent (tool-use, skills integration)
   - Attachment cards for embedded .docx/.pdf documents
   - Document status tracking (unsigned → sent → signed)
   - WYSIWYG document preview (docx-preview + JSZip for .docx, pdf.js for .pdf)
   - Upload signed PDF directly from attachment card
   - H1 auto-summary of all document statuses across WPs
   - Search with Ctrl+F shortcut
   - Draggable resizer

## CDN Dependencies

The viewer loads these libraries from CDN (no npm install needed):

| Library | Version | Purpose |
|---------|---------|---------|
| Toast UI Editor | 3.2.2 | WYSIWYG markdown editing |
| Marked.js | Latest | Markdown to HTML rendering |
| pdf.js | 3.11.174 | PDF page rendering for signed document previews |
| JSZip | 3.10.1 | Required by docx-preview to unzip .docx files |
| docx-preview | 0.3.3 | Renders .docx files as HTML for WYSIWYG preview |

**Load order matters:** JSZip must be loaded before docx-preview.

4. **`master_data.json`** - Variable store:
   - Company identity (name, reg no, FYE, framework)
   - Key financial figures (revenue, assets, liabilities)
   - Audit information (firm, partner, materiality)

## Audit Section Structure

| Section | Folder | Description |
|---------|--------|-------------|
| A | A_Planning | Planning & risk assessment |
| B | B_Internal_Control | Internal control evaluation |
| C | C_Assets | Assets testing (PPE, receivables, bank, inventory) |
| D | D_Liabilities_Equity | Liabilities & equity testing |
| E | E_Income_Statement | Revenue & expenses testing |
| F | F_Completion | Going concern, subsequent events, related parties |
| G | G_Outstanding | PBC items, queries, outstanding matters |

## Variable System

Variables use `{{variable_name}}` syntax in markdown files. Modifiers control formatting:

| Modifier | Example | Output |
|----------|---------|--------|
| (none) | `{{revenue}}` | 1,234,567.00 |
| `currency` | `{{revenue\|currency}}` | 1,234,567.00 |
| `rm` | `{{revenue\|rm}}` | RM 1,234,567.00 |
| `bracket` | `{{amount\|bracket}}` | (1,234.00) if negative |
| `rm_bracket` | `{{amount\|rm_bracket}}` | RM (1,234.00) if negative |
| `nil` | `{{amount\|nil}}` | NIL if zero |
| `text` | `{{company_name\|text}}` | Plain text |
| `raw` | `{{amount\|raw}}` | Raw number |

Variables with a `formula` field are calculated and shown as read-only with formula breakdown.

## Generation Instructions

When generating viewer files for a client:

1. Copy templates from VIEWER_TEMPLATE.md
2. Replace all `[CLIENT_NAME]` placeholders with actual client name
3. Replace `[COMPANY_NUMBER]` with registration number
4. Replace `[FYE_DATE]` with financial year end date
5. Replace `[REPORTING_FRAMEWORK]` with MPERS or MFRS
6. Sidebar auto-discovers files from `/api/files` — no manual sections array update needed
7. Populate `master_data.json` with client-specific variables
8. Verify all 4 files are generated in the client's engagement folder
