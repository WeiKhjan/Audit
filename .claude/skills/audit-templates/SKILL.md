---
name: templates
description: Generate standard audit letters and document templates pre-filled with engagement data for Malaysian statutory audits
---

# Audit Letter & Document Templates (.docx)

## Trigger

`/templates [type]` where `type` is one of:

| Type | Generates |
|------|-----------|
| `all` | All 16 templates (T1-T16) as .docx files |
| `engagement` | Group A: T1, T2, T3 |
| `confirmations` | Group B: T4, T5, T6, T7, T8, T9, T10, T15, T16 |
| `completion` | Group C: T11, T12 |
| `differences` | Group D: T13, T14 |
| `T1` through `T16` | Individual template by code |

## How It Works

Templates are generated as **Word .docx files** using `generate_templates.py` (skill asset). The script:

1. Reads `master_data.json` for variable substitution
2. Creates well-formatted .docx files using python-docx (letterhead, tables, signature blocks)
3. Places each .docx in the correct section folder alongside its parent working paper
4. Outputs `<!-- ATTACHMENT:{...} -->` comments that Claude inserts into the relevant WPs

## Template-to-WP Mapping

| Ref | Template | Embed in WP | Output Folder | Output Filename |
|-----|----------|-------------|---------------|-----------------|
| T1 | Engagement Letter | A1 | A_Planning | A1_Engagement_Letter.docx |
| T2 | PBC Request Letter | H1 | H_Engagement_Tracker | H1_PBC_Request_Letter.docx |
| T3 | Management Letter | standalone | F_Completion | F_Management_Letter.docx |
| T4 | Bank Confirmation | C9 | C_Assets | C9_Bank_Confirmation_{bank}.docx |
| T5 | Bank Authorization | C9 | C_Assets | C9_Bank_Authorization_{bank}.docx |
| T6 | Debtor Confirmation | C6 | C_Assets | C6_Debtor_Confirmation_{name}.docx |
| T7 | Creditor Confirmation | D8 | D_Liabilities_Equity | D8_Creditor_Confirmation_{name}.docx |
| T8 | Director Confirmation | D9 | D_Liabilities_Equity | D9_Director_Confirmation_{director}.docx |
| T9 | Legal Confirmation | standalone | F_Completion | F_Legal_Confirmation.docx |
| T10 | Stock Confirmation | C5 | C_Assets | C5_Stock_Confirmation.docx |
| T11 | MRL | F7 | F_Completion | F7_Management_Representation.docx |
| T12 | Director Support | F1 | F_Completion | F1_Director_Support_Letter.docx |
| T13 | Audit Adjustments | F6 | F_Completion | F6_Audit_Adjustments.docx |
| T14 | Uncorrected Diffs | F6 | F_Completion | F6_Uncorrected_Differences.docx |
| T15 | Directors Remuneration | F3 | F_Completion | F3_Director_Remuneration_{director}.docx |
| T16 | Directors Shareholding | F3 | F_Completion | F3_Director_Shareholding_{director}.docx |

Per-instance templates: T4/T5 per bank, T6 per debtor, T7 per creditor, T8/T15/T16 per director.

**Note:** T2 (PBC Request Letter) auto-populates from H1 PBC checklist. Generate via `/templates T2` after H1 is created (see `/pbc`).

## ATTACHMENT Comment Syntax

Embedded in working paper .md files:

```
<!-- ATTACHMENT:{"ref":"T8","title":"Director Confirmation - Cho Chin Lai","file":"D9_Director_Confirmation_CCL.docx","signed_file":"","status":"unsigned","date_prepared":"2026-03-08","date_sent":"","date_signed":""} -->
```

**Status flow:** `unsigned` → `sent` → `signed`

Multiple ATTACHMENT comments per WP are supported (e.g., C9 has T4 + T5, F6 has T13 + T14).

## Workflow

When `/templates` is invoked:

1. Copy `generate_templates.py` from skill folder to engagement folder (if not already there)
2. Run `python generate_templates.py all` (or specific templates)
3. Script generates .docx files and outputs ATTACHMENT JSON
4. Insert `<!-- ATTACHMENT:{...} -->` comments into the relevant WPs
5. Add `<!-- ATTACHMENT_SUMMARY -->` marker to H1 if not present

## Document Lifecycle

1. **Generated** — .docx created by script, ATTACHMENT status = `unsigned`
2. **Sent** — Auditor sends .docx to recipient, status updated to `sent` with date
3. **Signed** — Signed PDF returned and uploaded via viewer, status = `signed`

The viewer shows attachment cards with download, send, and upload actions. H1 shows a live summary of all document statuses across all WPs.

## Dependency

`python-docx` must be installed: `pip install python-docx`

## Script Location

`.claude/skills/audit-templates/generate_templates.py`

## Templates Detail

### Group A — Auditor-to-Client Letters

| Ref | Template | ISA | Description |
|-----|----------|-----|-------------|
| T1 | Engagement Letter | ISA 210 | Terms of audit engagement, responsibilities |
| T2 | PBC Request Letter | — | Request for 42 documents/information items |
| T3 | Management Letter | ISA 265 | Communication of internal control deficiencies |

### Group B — External Confirmations

| Ref | Template | ISA | Description |
|-----|----------|-----|-------------|
| T4 | Bank Confirmation | ISA 505 | Positive confirmation to bank (accounts, facilities, guarantees) |
| T5 | Bank Authorization | ISA 505 | Director authorization for bank to release info |
| T6 | Debtor Confirmation | ISA 505 | Positive confirmation of loan balances |
| T7 | Creditor Confirmation | ISA 505 | Negative confirmation of payable balances |
| T8 | Director Confirmation | ISA 550 | Balance, transaction, RPT declarations per director |
| T9 | Legal Confirmation | ISA 501 | Litigation, claims, legal fee confirmation |
| T10 | Stock Confirmation | ISA 505 | Inventory held by third parties (N/A for money lenders) |
| T15 | Directors Remuneration | CA 2016 s.230 | Per-director remuneration breakdown |
| T16 | Directors Shareholding | CA 2016 s.59 | Per-director shareholding confirmation |

### Group C — Completion Documents

| Ref | Template | ISA | Description |
|-----|----------|-----|-------------|
| T11 | MRL | ISA 580 | 38 representations covering all ISA areas |
| T12 | Director Support | ISA 570 | Undertaking for continued financial support |

### Group D — Audit Differences

| Ref | Template | ISA | Description |
|-----|----------|-----|-------------|
| T13 | Audit Adjustments | ISA 450 | Agreed adjustments schedule with impact summary |
| T14 | Uncorrected Differences | ISA 450 | Unadjusted items with materiality comparison |
