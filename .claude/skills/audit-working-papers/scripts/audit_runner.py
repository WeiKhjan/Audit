"""
AUDIT RUNNER - MAIN ORCHESTRATION SCRIPT
=========================================
Central script for running audit procedures and generating outputs.
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from excel_utils import (
    create_lead_schedule,
    create_ppe_schedule,
    create_bank_reconciliation,
    create_trial_balance_template,
    create_pbc_checklist,
    create_query_list,
    read_trial_balance
)

from word_utils import (
    create_financial_statements,
    create_management_letter,
    create_representation_letter
)


class AuditEngagement:
    """
    Class to manage an audit engagement.
    """

    def __init__(
        self,
        client_name: str,
        company_no: str,
        year_end: str,
        output_dir: str,
        reporting_framework: str = "MPERS"
    ):
        self.client_name = client_name
        self.company_no = company_no
        self.year_end = year_end
        self.output_dir = Path(output_dir)
        self.reporting_framework = reporting_framework

        # Create output directories
        self.awp_dir = self.output_dir / "AWP"
        self.fs_dir = self.output_dir / "FS"
        self.pbc_dir = self.output_dir / "PBC"

        for dir_path in [self.awp_dir, self.fs_dir, self.pbc_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Initialize data storage
        self.trial_balance = []
        self.queries = []
        self.adjustments = []
        self.pbc_items = []

        print(f"Audit engagement initialized for: {client_name}")
        print(f"Year end: {year_end}")
        print(f"Output directory: {output_dir}")

    def load_trial_balance(self, filepath: str, sheet_name: str = None):
        """Load trial balance from Excel file."""
        try:
            df = pd.read_excel(filepath, sheet_name=sheet_name or 0)
            self.trial_balance_df = df
            print(f"Trial balance loaded from: {filepath}")
            return df
        except Exception as e:
            print(f"Error loading trial balance: {e}")
            return None

    def load_ledger(self, filepath: str, sheet_name: str = None):
        """Load general ledger from Excel file."""
        try:
            df = pd.read_excel(filepath, sheet_name=sheet_name or 0)
            self.ledger_df = df
            print(f"Ledger loaded from: {filepath}")
            return df
        except Exception as e:
            print(f"Error loading ledger: {e}")
            return None

    def add_query(self, wp_ref: str, description: str, raised_by: str = "Auditor"):
        """Add an audit query."""
        self.queries.append({
            'wp_ref': wp_ref,
            'description': description,
            'raised_by': raised_by,
            'date_raised': datetime.now().strftime("%d/%m/%Y"),
            'response': '',
            'status': 'Open'
        })
        print(f"Query added: {wp_ref} - {description[:50]}...")

    def add_adjustment(
        self,
        description: str,
        debit_account: str,
        debit_amount: float,
        credit_account: str,
        credit_amount: float,
        adjusted: bool = False
    ):
        """Add an audit adjustment."""
        self.adjustments.append({
            'description': description,
            'debit_account': debit_account,
            'debit_amount': debit_amount,
            'credit_account': credit_account,
            'credit_amount': credit_amount,
            'adjusted': adjusted
        })
        status = "Adjusted" if adjusted else "Proposed"
        print(f"Adjustment added ({status}): {description}")

    # =========================================================================
    # WORKING PAPER GENERATION
    # =========================================================================

    def generate_awp_index(self):
        """Generate AWP index file."""
        filepath = self.awp_dir / "00_AWP_INDEX.xlsx"

        index_data = [
            {'Ref': 'A1', 'Description': 'Engagement Letter', 'Status': 'PBC', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'A2', 'Description': 'Planning Memorandum', 'Status': 'To Prepare', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'A3', 'Description': 'Risk Assessment', 'Status': 'To Prepare', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'A4', 'Description': 'Materiality', 'Status': 'To Prepare', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'B1', 'Description': 'Internal Control', 'Status': 'To Prepare', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'C1', 'Description': 'Property, Plant & Equipment', 'Status': 'In Progress', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'C2', 'Description': 'Cash & Bank', 'Status': 'In Progress', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'C3', 'Description': 'Trade Receivables', 'Status': 'To Prepare', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'C4', 'Description': 'Other Receivables & Prepayments', 'Status': 'In Progress', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'D1', 'Description': 'Share Capital', 'Status': 'To Prepare', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'D2', 'Description': 'Retained Earnings', 'Status': 'To Prepare', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'D3', 'Description': 'Trade Payables', 'Status': 'In Progress', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'D4', 'Description': 'Other Payables & Accruals', 'Status': 'In Progress', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'D5', 'Description': 'Amount Due to Directors', 'Status': 'In Progress', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'D6', 'Description': 'Amount Due to Related Parties', 'Status': 'In Progress', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'E1', 'Description': 'Revenue', 'Status': 'To Prepare', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'E2', 'Description': 'Cost of Sales', 'Status': 'To Prepare', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'E3', 'Description': 'Other Income', 'Status': 'In Progress', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'E4', 'Description': 'Administrative Expenses', 'Status': 'In Progress', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'E5', 'Description': 'Tax Expense', 'Status': 'To Prepare', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'F1', 'Description': 'Going Concern', 'Status': 'To Prepare', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'F2', 'Description': 'Subsequent Events', 'Status': 'To Prepare', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'F3', 'Description': 'Related Party Transactions', 'Status': 'In Progress', 'Preparer': '', 'Reviewer': ''},
            {'Ref': 'F4', 'Description': 'Completion Checklist', 'Status': 'To Prepare', 'Preparer': '', 'Reviewer': ''},
        ]

        create_lead_schedule(
            filepath=str(filepath),
            client_name=self.client_name,
            year_end=self.year_end,
            subject="AUDIT WORKING PAPER INDEX",
            wp_ref="INDEX",
            data=index_data,
            columns=['Ref', 'Description', 'Status', 'Preparer', 'Reviewer']
        )
        return filepath

    def generate_ppe_schedule(self, assets: list):
        """Generate PPE working paper."""
        filepath = self.awp_dir / "C1_PPE_Schedule.xlsx"
        create_ppe_schedule(
            filepath=str(filepath),
            client_name=self.client_name,
            year_end=self.year_end,
            assets=assets
        )
        return filepath

    def generate_bank_recon(
        self,
        bank_name: str,
        account_number: str,
        balance_per_bank: float,
        balance_per_books: float,
        unpresented_cheques: list = None,
        uncredited_deposits: list = None
    ):
        """Generate bank reconciliation working paper."""
        filepath = self.awp_dir / "C2_Bank_Reconciliation.xlsx"
        create_bank_reconciliation(
            filepath=str(filepath),
            client_name=self.client_name,
            year_end=self.year_end,
            bank_name=bank_name,
            account_number=account_number,
            balance_per_bank=balance_per_bank,
            balance_per_books=balance_per_books,
            unpresented_cheques=unpresented_cheques or [],
            uncredited_deposits=uncredited_deposits or []
        )
        return filepath

    def generate_pbc_checklist(self, custom_items: list = None):
        """Generate PBC checklist."""
        filepath = self.pbc_dir / "PBC_Checklist.xlsx"
        create_pbc_checklist(
            filepath=str(filepath),
            client_name=self.client_name,
            year_end=self.year_end,
            items=custom_items
        )
        return filepath

    def generate_query_list(self):
        """Generate query tracking list."""
        filepath = self.awp_dir / "00_Outstanding_Queries.xlsx"
        create_query_list(
            filepath=str(filepath),
            client_name=self.client_name,
            year_end=self.year_end,
            queries=self.queries
        )
        return filepath

    # =========================================================================
    # FINANCIAL STATEMENTS GENERATION
    # =========================================================================

    def generate_draft_fs(self, data: dict = None):
        """Generate draft financial statements."""
        filepath = self.fs_dir / f"FS_DRAFT_{self.client_name.replace(' ', '_')}.docx"
        create_financial_statements(
            filepath=str(filepath),
            company_name=self.client_name,
            company_no=self.company_no,
            year_end=self.year_end,
            reporting_framework=self.reporting_framework,
            data=data
        )
        return filepath

    def generate_management_letter(self, findings: list, auditor_firm: str):
        """Generate management letter."""
        filepath = self.fs_dir / "Management_Letter.docx"
        create_management_letter(
            filepath=str(filepath),
            company_name=self.client_name,
            year_end=self.year_end,
            findings=findings,
            auditor_firm=auditor_firm
        )
        return filepath

    def generate_rep_letter(self, auditor_firm: str, directors: list):
        """Generate representation letter."""
        filepath = self.fs_dir / "Representation_Letter.docx"
        create_representation_letter(
            filepath=str(filepath),
            company_name=self.client_name,
            company_no=self.company_no,
            year_end=self.year_end,
            auditor_firm=auditor_firm,
            directors=directors
        )
        return filepath

    # =========================================================================
    # SUMMARY & REPORTING
    # =========================================================================

    def generate_engagement_summary(self):
        """Generate engagement summary report."""
        summary = f"""
================================================================================
AUDIT ENGAGEMENT SUMMARY
================================================================================
Client:              {self.client_name}
Company No:          {self.company_no}
Year End:            {self.year_end}
Reporting Framework: {self.reporting_framework}
Generated:           {datetime.now().strftime("%d/%m/%Y %H:%M")}
================================================================================

OUTSTANDING QUERIES: {len(self.queries)}
--------------------------------------------------------------------------------
"""
        for idx, q in enumerate(self.queries, 1):
            summary += f"{idx}. [{q['wp_ref']}] {q['description'][:60]}... ({q['status']})\n"

        summary += f"""
--------------------------------------------------------------------------------

PROPOSED ADJUSTMENTS: {len([a for a in self.adjustments if not a['adjusted']])}
PROCESSED ADJUSTMENTS: {len([a for a in self.adjustments if a['adjusted']])}
--------------------------------------------------------------------------------
"""
        for idx, a in enumerate(self.adjustments, 1):
            status = "ADJUSTED" if a['adjusted'] else "PROPOSED"
            summary += f"{idx}. [{status}] {a['description']}\n"
            summary += f"   DR {a['debit_account']}: RM{a['debit_amount']:,.2f}\n"
            summary += f"   CR {a['credit_account']}: RM{a['credit_amount']:,.2f}\n"

        summary += """
================================================================================
"""
        print(summary)

        # Save to file
        filepath = self.output_dir / "Engagement_Summary.txt"
        with open(filepath, 'w') as f:
            f.write(summary)

        return summary


def main():
    """Main entry point for command-line usage."""
    print("=" * 60)
    print("AUDIT RUNNER - Malaysian Statutory Audit Tools")
    print("=" * 60)
    print()
    print("Usage:")
    print("  from audit_runner import AuditEngagement")
    print()
    print("  engagement = AuditEngagement(")
    print("      client_name='Company Name Sdn. Bhd.',")
    print("      company_no='123456-X',")
    print("      year_end='31 December 2024',")
    print("      output_dir='./audit_output'")
    print("  )")
    print()
    print("Available methods:")
    print("  - engagement.load_trial_balance(filepath)")
    print("  - engagement.load_ledger(filepath)")
    print("  - engagement.add_query(wp_ref, description)")
    print("  - engagement.add_adjustment(...)")
    print("  - engagement.generate_awp_index()")
    print("  - engagement.generate_ppe_schedule(assets)")
    print("  - engagement.generate_bank_recon(...)")
    print("  - engagement.generate_pbc_checklist()")
    print("  - engagement.generate_query_list()")
    print("  - engagement.generate_draft_fs()")
    print("  - engagement.generate_management_letter(findings, firm)")
    print("  - engagement.generate_rep_letter(firm, directors)")
    print("  - engagement.generate_engagement_summary()")


if __name__ == "__main__":
    main()
