#!/usr/bin/env python3
"""
IRS Tax Form Formatter
Converts JSON tax data into formatted text files that resemble actual IRS forms
"""

import json
import os
from datetime import datetime

def format_currency(amount):
    """Format number as currency"""
    if amount < 0:
        return f"({abs(amount):,.2f})"
    return f"{amount:,.2f}"

def format_form_1040(data, output_file):
    """Format Form 1040 as text"""
    form = data['form_1040']
    taxpayer = form['taxpayer']

    content = f"""
================================================================================
                        U.S. Individual Income Tax Return
                               Form 1040
                          Tax Year {form['tax_year']}
================================================================================

Department of the Treasury - Internal Revenue Service

Filing Status:  {form['filing_status']}

Name and Address:
  {taxpayer['name']}
  SSN: {taxpayer['ssn']}
  State: {taxpayer['address']['state']}
"""

    if form.get('spouse'):
        content += f"""
Spouse Information:
  {form['spouse']['name']}
  SSN: {form['spouse']['ssn']}
"""

    content += f"""
================================================================================
                                   INCOME
================================================================================

1.  Wages, salaries, tips, etc.                        ${format_currency(form['wages_salaries'])}
2a. Tax-exempt interest                                ${format_currency(0)}
2b. Taxable interest                                   ${format_currency(form['interest_income'])}
3a. Qualified dividends                                ${format_currency(0)}
3b. Ordinary dividends                                 ${format_currency(form['dividend_income'])}
4.  IRA distributions                                  ${format_currency(0)}
5.  Pensions and annuities                             ${format_currency(0)}
6.  Social security benefits                           ${format_currency(0)}
7.  Capital gain or (loss)                             ${format_currency(form['capital_gains'])}
8.  Schedule 1, Additional Income                      ${format_currency(form['business_income'])}

                                                       ─────────────────
9.  TOTAL INCOME                                       ${format_currency(form['total_income'])}
                                                       ─────────────────

================================================================================
                    ADJUSTMENTS TO INCOME
================================================================================

10a. Deductible part of self-employment tax            ${format_currency(form['self_employment_tax_deduction'])}
10b. Self-employed SEP, SIMPLE, qualified plans        ${format_currency(form['sep_ira_deduction'])}
10c. Self-employed health insurance deduction          ${format_currency(form.get('health_insurance_deduction', 0))}
10d. Other adjustments                                 ${format_currency(0)}

                                                       ─────────────────
11.  Total adjustments                                 ${format_currency(form['total_adjustments'])}
                                                       ─────────────────

12.  ADJUSTED GROSS INCOME (AGI)                       ${format_currency(form['adjusted_gross_income'])}
                                                       =================

================================================================================
                    STANDARD DEDUCTION
================================================================================

13.  Standard deduction or itemized deductions         ${format_currency(form['standard_deduction'])}

14.  TAXABLE INCOME                                    ${format_currency(form['taxable_income'])}
                                                       =================

================================================================================
                            TAX AND CREDITS
================================================================================

15.  Federal income tax                                ${format_currency(form['federal_income_tax'])}
16.  Self-employment tax (Schedule SE)                 ${format_currency(form['self_employment_tax'])}

                                                       ─────────────────
17.  TOTAL TAX                                         ${format_currency(form['total_tax'])}
                                                       =================

================================================================================
                               PAYMENTS
================================================================================

18.  Federal income tax withheld                       ${format_currency(form['federal_withholding'])}
19.  Estimated tax payments                            ${format_currency(form['estimated_tax_payments'])}

                                                       ─────────────────
20.  Total payments                                    ${format_currency(form['estimated_tax_payments'])}
                                                       ─────────────────

================================================================================
                        REFUND OR AMOUNT YOU OWE
================================================================================

21.  Amount overpaid (REFUND)                          ${format_currency(max(0, form['refund_or_owed']))}
22.  Amount you owe                                    ${format_currency(abs(min(0, form['refund_or_owed'])))}

================================================================================

Sign     Under penalties of perjury, I declare that I have examined this return
Here     and accompanying schedules and statements, and to the best of my knowledge
         and belief, they are true, correct, and complete.

Your signature __________________ Date __________
Spouse's signature __________________ Date __________

================================================================================
                    For IRS Use Only - Do Not Write in This Space
================================================================================
"""

    with open(output_file, 'w') as f:
        f.write(content)

def format_schedule_c(full_data, output_file):
    """Format Schedule C as text"""
    form = full_data['schedule_c']
    business_info = full_data.get('business_info', {})

    # Extract owner info from form data if not in business_info
    owner_name = business_info.get('Owner 1 Name', 'Taxpayer Name')
    owner_ssn = business_info.get('Owner 1 SSN', 'XXX-XX-XXXX')
    industry = business_info.get('Industry', form.get('principal_business_code', 'Business'))

    content = f"""
================================================================================
                        SCHEDULE C
                (Form 1040)
         Profit or Loss From Business
         (Sole Proprietorship)
================================================================================

                          Tax Year {form['tax_year']}

Department of the Treasury
Internal Revenue Service (99)

Name of proprietor: {owner_name}
Social Security Number: {owner_ssn}

A.  Principal business or profession: {industry}
B.  Business name: {form['business_name']}
C.  Business address: {form['business_address']['state']}
D.  Employer ID number (EIN): {form['ein']}
E.  Business code: {form['principal_business_code']}
F.  Accounting method: {form['accounting_method']}
G.  Did you "materially participate" in the operation of this business? Yes [X] No [ ]

================================================================================
                            PART I - INCOME
================================================================================

1.  Gross receipts or sales                            ${format_currency(form['gross_receipts'])}
2.  Returns and allowances                             ${format_currency(form['returns_allowances'])}
3.  Subtract line 2 from line 1                        ${format_currency(form['gross_receipts'])}
4.  Cost of goods sold (from Part III)                 ${format_currency(form['cost_of_goods_sold'])}
                                                       ─────────────────
5.  Gross profit (subtract line 4 from line 3)         ${format_currency(form['gross_profit'])}
                                                       ─────────────────
6.  Other income                                       ${format_currency(form['other_income'])}
                                                       ─────────────────
7.  GROSS INCOME (add lines 5 and 6)                   ${format_currency(form['gross_income'])}
                                                       =================

================================================================================
                        PART II - EXPENSES
================================================================================

8.  Advertising                                        ${format_currency(form['expenses']['advertising'])}
9.  Car and truck expenses                             ${format_currency(form['expenses']['car_truck'])}
10. Commissions and fees                               ${format_currency(form['expenses']['commissions_fees'])}
11. Contract labor                                     ${format_currency(form['expenses']['contract_labor'])}
12. Depletion                                          ${format_currency(form['expenses']['depletion'])}
13. Depreciation                                       ${format_currency(form['expenses']['depreciation'])}
14. Employee benefit programs                          ${format_currency(form['expenses']['employee_benefit_programs'])}
15. Insurance (other than health)                      ${format_currency(form['expenses']['insurance'])}
16. Interest:
    a. Mortgage (paid to banks, etc.)                  ${format_currency(form['expenses']['interest_mortgage'])}
    b. Other                                           ${format_currency(form['expenses']['interest_other'])}
17. Legal and professional services                    ${format_currency(form['expenses']['legal_professional'])}
18. Office expense                                     ${format_currency(form['expenses']['office_expense'])}
19. Pension and profit-sharing plans                   ${format_currency(form['expenses']['pension_profit_sharing'])}
20. Rent or lease:
    a. Vehicles, machinery, equipment                  ${format_currency(form['expenses']['rent_lease_vehicles'])}
    b. Other business property                         ${format_currency(form['expenses']['rent_lease_property'])}
21. Repairs and maintenance                            ${format_currency(form['expenses']['repairs_maintenance'])}
22. Supplies                                           ${format_currency(form['expenses']['supplies'])}
23. Taxes and licenses                                 ${format_currency(form['expenses']['taxes_licenses'])}
24. Travel and meals:
    a. Travel                                          ${format_currency(form['expenses']['travel'])}
    b. Deductible meals                                ${format_currency(form['expenses']['deductible_meals'])}
25. Utilities                                          ${format_currency(form['expenses']['utilities'])}
26. Wages (less employment credits)                    ${format_currency(form['expenses']['wages'])}
27. Other expenses                                     ${format_currency(form['expenses']['other_expenses'])}

                                                       ─────────────────
28. Total expenses (add lines 8 through 27)            ${format_currency(form['total_expenses'])}
                                                       =================

================================================================================
                            NET PROFIT OR LOSS
================================================================================

29. Tentative profit or (loss) (line 7 minus 28)       ${format_currency(form['tentative_profit'])}

30. Expenses for business use of your home             ${format_currency(0)}

31. NET PROFIT OR (LOSS)                               ${format_currency(form['net_profit_loss'])}
    (subtract line 30 from line 29)                    =================

    If a profit, enter on Form 1040, line 8, and also on Schedule SE, line 2.
    If a loss, you must go to line 32.

================================================================================

For Paperwork Reduction Act Notice, see your tax return instructions.
Cat. No. 11334P                                        Schedule C (Form 1040)

================================================================================
"""

    with open(output_file, 'w') as f:
        f.write(content)

def format_form_1120s(data, output_file):
    """Format Form 1120-S as text"""
    form = data['form_1120s']
    beg_bs = form['balance_sheet']['beginning_of_year']
    end_bs = form['balance_sheet']['end_of_year']

    content = f"""
================================================================================
                        U.S. Income Tax Return for an S Corporation
                               Form 1120-S
                          Tax Year {form['tax_year']}
================================================================================

Department of the Treasury
Internal Revenue Service

A.  S election effective date: {form['date_incorporated']}
B.  Business activity code: {form['business_code']}
C.  Employer identification number: {form['ein']}

Corporation Name: {form['corporation_name']}
State of incorporation: {form['state_of_incorporation']}
Date incorporated: {form['date_incorporated']}

================================================================================
                        INCOME
================================================================================

1a. Gross receipts or sales                            ${format_currency(form['gross_receipts'])}
1b. Returns and allowances                             ${format_currency(form['returns_allowances'])}
1c. Balance (subtract 1b from 1a)                      ${format_currency(form['gross_receipts'])}
2.  Cost of goods sold (Schedule A)                    ${format_currency(form['cost_of_goods_sold'])}
                                                       ─────────────────
3.  Gross profit (subtract line 2 from 1c)             ${format_currency(form['gross_profit'])}
                                                       ─────────────────
4.  Net gain (loss) from Form 4797                     ${format_currency(form['net_gain_loss'])}
5.  Other income                                       ${format_currency(form['other_income'])}
                                                       ─────────────────
6.  TOTAL INCOME (add lines 3, 4, and 5)               ${format_currency(form['total_income'])}
                                                       =================

================================================================================
                        DEDUCTIONS
================================================================================

7.  Compensation of officers                           ${format_currency(form['compensation_officers'])}
8.  Salaries and wages                                 ${format_currency(form['salaries_wages'])}
9.  Repairs and maintenance                            ${format_currency(form['repairs_maintenance'])}
10. Bad debts                                          ${format_currency(form['bad_debts'])}
11. Rents                                              ${format_currency(form['rents'])}
12. Taxes and licenses                                 ${format_currency(form['taxes_licenses'])}
13. Interest                                           ${format_currency(form['interest'])}
14. Depreciation                                       ${format_currency(form['depreciation'])}
15. Advertising                                        ${format_currency(form['advertising'])}
16. Pension, profit-sharing, etc., plans               ${format_currency(form['pension_plans'])}
17. Employee benefit programs                          ${format_currency(form['employee_benefits'])}
18. Other deductions                                   ${format_currency(form['other_deductions'])}

                                                       ─────────────────
19. TOTAL DEDUCTIONS (add lines 7 through 18)          ${format_currency(form['total_deductions'])}
                                                       =================

20. ORDINARY BUSINESS INCOME (LOSS)                    ${format_currency(form['ordinary_business_income'])}
    (subtract line 19 from line 6)                     =================

================================================================================
                    SCHEDULE K - DISTRIBUTIVE SHARE ITEMS
================================================================================

1.  Ordinary business income (loss) (page 1, line 20)  ${format_currency(form['schedule_k']['ordinary_income'])}
2.  Net rental real estate income (loss)               ${format_currency(form['schedule_k']['rental_real_estate_income'])}
3.  Other net rental income (loss)                     ${format_currency(form['schedule_k']['other_rental_income'])}
4.  Interest income                                    ${format_currency(form['schedule_k']['interest_income'])}
5.  Dividends                                          ${format_currency(form['schedule_k']['dividends'])}
6.  Royalties                                          ${format_currency(form['schedule_k']['royalties'])}
7.  Net short-term capital gain (loss)                 ${format_currency(form['schedule_k']['net_short_term_capital_gain'])}
8.  Net long-term capital gain (loss)                  ${format_currency(form['schedule_k']['net_long_term_capital_gain'])}
9.  Other income (loss)                                ${format_currency(form['schedule_k']['other_income'])}

================================================================================
                    SCHEDULE L - BALANCE SHEETS
================================================================================

ASSETS                                    Beginning of Year    End of Year
────────────────────────────────────────────────────────────────────────────
Cash                                      ${format_currency(beg_bs['assets']['cash']):>15}    ${format_currency(end_bs['assets']['cash']):>15}
Accounts receivable                       ${format_currency(beg_bs['assets']['accounts_receivable']):>15}    ${format_currency(end_bs['assets']['accounts_receivable']):>15}
Inventory                                 ${format_currency(beg_bs['assets']['inventory']):>15}    ${format_currency(end_bs['assets']['inventory']):>15}
Other current assets                      ${format_currency(beg_bs['assets']['other_current_assets']):>15}    ${format_currency(end_bs['assets']['other_current_assets']):>15}
Fixed assets (net)                        ${format_currency(beg_bs['assets']['fixed_assets'] - beg_bs['assets']['accumulated_depreciation']):>15}    ${format_currency(end_bs['assets']['fixed_assets'] - end_bs['assets']['accumulated_depreciation']):>15}
Other assets                              ${format_currency(beg_bs['assets']['other_assets']):>15}    ${format_currency(end_bs['assets']['other_assets']):>15}
                                          ─────────────────    ─────────────────
TOTAL ASSETS                              ${format_currency(beg_bs['assets']['total_assets']):>15}    ${format_currency(end_bs['assets']['total_assets']):>15}
                                          =================    =================

LIABILITIES AND SHAREHOLDERS' EQUITY
────────────────────────────────────────────────────────────────────────────
Accounts payable                          ${format_currency(beg_bs['liabilities_equity']['accounts_payable']):>15}    ${format_currency(end_bs['liabilities_equity']['accounts_payable']):>15}
Current portion long-term debt            ${format_currency(beg_bs['liabilities_equity']['current_portion_long_term_debt']):>15}    ${format_currency(end_bs['liabilities_equity']['current_portion_long_term_debt']):>15}
Other current liabilities                 ${format_currency(beg_bs['liabilities_equity']['other_current_liabilities']):>15}    ${format_currency(end_bs['liabilities_equity']['other_current_liabilities']):>15}
Long-term debt                            ${format_currency(beg_bs['liabilities_equity']['long_term_debt']):>15}    ${format_currency(end_bs['liabilities_equity']['long_term_debt']):>15}
Capital stock                             ${format_currency(beg_bs['liabilities_equity']['capital_stock']):>15}    ${format_currency(end_bs['liabilities_equity']['capital_stock']):>15}
Retained earnings                         ${format_currency(beg_bs['liabilities_equity']['retained_earnings']):>15}    ${format_currency(end_bs['liabilities_equity']['retained_earnings']):>15}
                                          ─────────────────    ─────────────────
TOTAL LIABILITIES & EQUITY                ${format_currency(beg_bs['liabilities_equity']['total_liabilities_equity']):>15}    ${format_currency(end_bs['liabilities_equity']['total_liabilities_equity']):>15}
                                          =================    =================

================================================================================

For Paperwork Reduction Act Notice, see separate instructions.
Cat. No. 11510H                                        Form 1120-S (2023)

================================================================================
"""

    with open(output_file, 'w') as f:
        f.write(content)

def format_schedule_k1(data, output_file, owner_num=1):
    """Format Schedule K-1 as text"""
    form_key = f'schedule_k1_owner{owner_num}'
    if form_key not in data:
        return

    form = data[form_key]
    shareholder = form['shareholder']

    content = f"""
================================================================================
                        Schedule K-1
                      (Form 1120-S)
        Shareholder's Share of Income, Deductions, Credits, etc.
================================================================================

                          Tax Year {form['tax_year']}

Department of the Treasury
Internal Revenue Service

Part I - Information About the Corporation

Corporation's name: {form['corporation_name']}
Corporation's EIN: {form['corporation_ein']}

Part II - Information About the Shareholder

Shareholder's name: {shareholder['name']}
Shareholder's SSN: {shareholder['ssn']}
Shareholder's percentage of stock ownership: {shareholder['ownership_percentage']}%

================================================================================
            Part III - Shareholder's Share of Current Year Income,
                      Deductions, Credits, and Other Items
================================================================================

                        INCOME (LOSS)

1.  Ordinary business income (loss)                    ${format_currency(form['shareholder_share_of_income']['ordinary_business_income'])}
2.  Net rental real estate income (loss)               ${format_currency(form['shareholder_share_of_income']['net_rental_real_estate_income'])}
3.  Other net rental income (loss)                     ${format_currency(form['shareholder_share_of_income']['other_net_rental_income'])}
4.  Interest income                                    ${format_currency(form['shareholder_share_of_income']['interest_income'])}
5.  Ordinary dividends                                 ${format_currency(form['shareholder_share_of_income']['dividends'])}
6.  Royalties                                          ${format_currency(form['shareholder_share_of_income']['royalties'])}
7.  Net short-term capital gain (loss)                 ${format_currency(form['shareholder_share_of_income']['net_short_term_capital_gain'])}
8.  Net long-term capital gain (loss)                  ${format_currency(form['shareholder_share_of_income']['net_long_term_capital_gain'])}

                        DEDUCTIONS

9.  Section 179 deduction                              ${format_currency(form['shareholder_share_of_deductions']['section_179_deduction'])}
10. Charitable contributions                           ${format_currency(form['shareholder_share_of_deductions']['charitable_contributions'])}
11. Investment interest expense                        ${format_currency(form['shareholder_share_of_deductions']['investment_interest'])}

================================================================================
            SHAREHOLDER'S CAPITAL ACCOUNT ANALYSIS
================================================================================

Beginning capital account                              ${format_currency(form['shareholder_capital_account']['beginning_capital'])}
Capital contributed during the year                    ${format_currency(form['shareholder_capital_account']['capital_contributed'])}
Current year net income (loss)                         ${format_currency(form['shareholder_capital_account']['current_year_income'])}
Other increase (decrease)                              ${format_currency(0)}
Withdrawals and distributions                          ${format_currency(form['shareholder_capital_account']['withdrawals_distributions'])}
                                                       ─────────────────
Ending capital account                                 ${format_currency(form['shareholder_capital_account']['ending_capital'])}
                                                       =================

================================================================================

For Paperwork Reduction Act Notice, see instructions for Form 1120-S.
Cat. No. 11520D                            Schedule K-1 (Form 1120-S) 2023

================================================================================
"""

    with open(output_file, 'w') as f:
        f.write(content)

def main():
    """Main function to format all tax returns"""
    tax_data_dir = os.path.join(os.path.dirname(__file__), 'tax_returns_data')
    output_dir = os.path.join(os.path.dirname(__file__), 'tax_returns_formatted')
    os.makedirs(output_dir, exist_ok=True)

    # Process each tax return JSON file
    for filename in os.listdir(tax_data_dir):
        if not filename.endswith('.json'):
            continue

        json_path = os.path.join(tax_data_dir, filename)

        with open(json_path, 'r') as f:
            data = json.load(f)

        business_name = data['business_info']['Business Name']
        print(f"\nFormatting tax forms for {business_name}...")

        base_name = filename.replace('.json', '')

        # Format based on entity type
        if 'form_1040' in data['forms']:
            # Sole proprietorship
            form_1040_path = os.path.join(output_dir, f"{base_name}_Form_1040.txt")
            format_form_1040(data['forms'], form_1040_path)
            print(f"  ✓ Form 1040: {form_1040_path}")

            schedule_c_path = os.path.join(output_dir, f"{base_name}_Schedule_C.txt")
            # Pass the entire data structure including business_info
            schedule_c_data = {
                'schedule_c': data['forms']['schedule_c'],
                'business_info': data['business_info']
            }
            format_schedule_c(schedule_c_data, schedule_c_path)
            print(f"  ✓ Schedule C: {schedule_c_path}")

        elif 'form_1120s' in data['forms']:
            # S-Corporation
            form_1120s_path = os.path.join(output_dir, f"{base_name}_Form_1120S.txt")
            format_form_1120s(data['forms'], form_1120s_path)
            print(f"  ✓ Form 1120-S: {form_1120s_path}")

            # K-1 for owner 1
            k1_owner1_path = os.path.join(output_dir, f"{base_name}_Schedule_K1_Owner1.txt")
            format_schedule_k1(data['forms'], k1_owner1_path, 1)
            print(f"  ✓ Schedule K-1 (Owner 1): {k1_owner1_path}")

            # K-1 for owner 2 if exists
            if 'schedule_k1_owner2' in data['forms']:
                k1_owner2_path = os.path.join(output_dir, f"{base_name}_Schedule_K1_Owner2.txt")
                format_schedule_k1(data['forms'], k1_owner2_path, 2)
                print(f"  ✓ Schedule K-1 (Owner 2): {k1_owner2_path}")

    print(f"\n✅ Tax form formatting complete!")
    print(f"   Output directory: {output_dir}")

if __name__ == "__main__":
    main()
