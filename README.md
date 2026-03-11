# Claude Audit Assistant - Malaysia

An AI-powered audit framework for Malaysian statutory audits, built on Claude Code with custom skills for generating working papers, financial statements, and interactive viewers.

## Prerequisites

Before using this codebase, install the following on your computer:

### 1. Python (Required)

- **Python 3.6 or later**
- Download from: https://www.python.org/downloads/
- During installation, **check "Add Python to PATH"**
- No additional Python packages needed — the project uses only the standard library

To verify installation, open a terminal and run:

```bash
python --version
```

### 2. Git (Required)

- **Git** for version control
- Download from: https://git-scm.com/downloads
- Needed to clone the repository and track changes

### 3. Claude Code CLI (Required)

- **Claude Code** — Anthropic's CLI tool for Claude
- Install via npm:

```bash
npm install -g @anthropic-ai/claude-code
```

- This requires **Node.js 18+** — download from: https://nodejs.org/
- Authenticate with your Anthropic account after installation

### 4. Anthropic API Key (Required for Viewer AI Features)

- Obtain from: https://console.anthropic.com
- The API key is entered in the browser UI when using the audit viewer
- The server proxies API calls to keep your key secure

### 5. Web Browser (Required)

- Any modern browser: **Chrome**, **Firefox**, **Edge**, or **Safari**
- Required to view the interactive audit viewer

## Installation Summary

| Software | Minimum Version | Purpose |
|----------|----------------|---------|
| Python | 3.6+ | Local HTTP server for the audit viewer |
| Git | Any recent | Version control |
| Node.js | 18+ | Required to install Claude Code CLI |
| Claude Code | Latest | AI assistant with audit skills |
| Web Browser | Modern | View interactive audit working papers |

> **Note:** No `pip install`, `npm install`, or `requirements.txt` is needed for the project itself. All frontend libraries (Toast UI Editor, Marked.js) are loaded from CDN. Python uses only standard library modules.

## Quick Start

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd "Pilot - Audit - Claude"
   ```

2. **Launch Claude Code**

   ```bash
   claude
   ```

3. **Start an engagement** — Use the available skills:

   | Command | Description |
   |---------|-------------|
   | `/materiality` | Calculate planning/performance materiality |
   | `/risk-assessment` | Perform risk assessment and identify red flags |
   | `/awp [area]` | Generate audit working papers (PPE, bank, receivables, etc.) |
   | `/fs [component]` | Draft financial statements (SOFP, SOCI, notes) |
   | `/pbc [action]` | Manage PBC checklist |
   | `/query [action]` | Manage audit queries |
   | `/viewer` | Generate interactive HTML viewer |

4. **View working papers** — Navigate to the client folder and double-click `START_VIEWER.bat`, or run:

   ```bash
   cd Clients/AWP_<ClientName>_FYE<Year>
   python server.py
   ```

   Then open http://localhost:8000/audit_viewer.html in your browser.

## Project Structure

```
Pilot - Audit - Claude/
├── CLAUDE.md                     # Project instructions & audit standards
├── README.md                     # This file
├── .claude/
│   ├── settings.local.json       # Claude Code permissions
│   └── skills/                   # Custom audit skills
│       ├── audit-working-papers/
│       ├── financial-statements/
│       ├── materiality-assessment/
│       ├── pbc-query-management/
│       ├── risk-assessment/
│       └── working-papers-viewer/
└── Clients/
    └── AWP_<ClientName>_FYE<Year>/
        ├── server.py             # Local HTTP server
        ├── audit_viewer.html     # Interactive viewer
        ├── START_VIEWER.bat      # Windows launcher
        ├── master_data.json      # Client variables
        ├── A_Planning/           # Planning & risk
        ├── B_Internal_Control/   # Control evaluation
        ├── C_Assets/             # Asset testing
        ├── D_Liabilities_Equity/ # Liability & equity
        ├── E_Income_Statement/   # Income & expense
        ├── F_Completion/         # Completion & review
        └── G_Outstanding/        # Outstanding items
```
