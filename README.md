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
   | `/sampling [area]` | Generate ISA 530 audit sampling papers (MUS calculation, selection, evaluation) |
   | `/templates [type]` | Generate audit letters & document templates (engagement letter, confirmations, MRL, etc.) |
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
│       ├── audit-working-papers/ # /awp — working papers with SAP & TOD framework
│       ├── audit-sampling/       # /sampling — ISA 530 MUS sampling
│       ├── audit-templates/      # /templates — letters & confirmations (T1-T16)
│       ├── financial-statements/ # /fs — MPERS/MFRS financial statements
│       ├── materiality-assessment/ # /materiality — PM, PerfM, trivial threshold
│       ├── pbc-query-management/ # /pbc, /query — PBC & audit query tracking
│       ├── risk-assessment/      # /risk-assessment — ISA 315 risk assessment
│       └── working-papers-viewer/ # /viewer — interactive HTML viewer
└── Clients/                      # (gitignored — confidential client data)
    └── AWP_<ClientName>_FYE<Year>/
        ├── server.py             # Local HTTP server
        ├── audit_viewer.html     # Interactive viewer with AI chat
        ├── START_VIEWER.bat      # Windows launcher
        ├── master_data.json      # Client variables ({{placeholders}})
        ├── 00_Index.md           # Working papers index & status dashboard
        ├── A_Planning/           # A1-A8: Planning, risk, materiality, strategy
        ├── B_Internal_Control/   # B1: ICQ, B2: Journal entry testing (ISA 240)
        ├── C_Assets/             # C1-C10: PPE, receivables, cash, etc.
        ├── D_Liabilities_Equity/ # D1-D12: Share capital, payables, tax, etc.
        ├── E_Income_Statement/   # E1-E8: Revenue (SAP+TOD), expenses (SAP/TOD)
        ├── F_Completion/         # F1-F9: Going concern, subsequent events, report
        ├── G_Financial_Statements/ # G1-G3: Directors' report, SOFP, SOCI
        └── T_Templates/          # T1-T16: Letters, confirmations, MRL, adjustments
```

## Key Features

- **Substantive Analytical Procedures (SAP)** — auto-computes expected amounts for predictable items (salaries × 12, EPF at statutory rate, depreciation from FAR) and compares to GL. Threshold = MAX(Performance Materiality, 5% of line item)
- **GL-Driven Auto-Population** — when the General Ledger is available, SAP tables and journal entry testing are populated automatically from source data
- **Journal Entry Testing (ISA 240)** — mandatory B2 working paper with 10 fraud risk selection criteria, estimate bias review, and unusual transaction evaluation
- **Clickable Cross-References** — working paper references (e.g., "See C6") are clickable links in the viewer, navigating directly to the referenced paper
- **16 Template Letters (T1-T16)** — engagement letter, bank/debtor/creditor/director/legal confirmations, MRL, director support letter, audit adjustments summaries, directors' remuneration & shareholding confirmations
- **ISA 530 Audit Sampling** — MUS calculation, systematic selection, and evaluation framework
- **`{{variable}}` Placeholder System** — all monetary figures use placeholders from `master_data.json`, resolved at render time in the viewer
- **Interactive Viewer** — single-page HTML app with markdown rendering, variable resolution, sidebar navigation, and AI-powered audit assistant chat
