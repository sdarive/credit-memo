#!/usr/bin/env python3
"""
IRS Tax Form Data Generator
Generates realistic tax return data for testing credit memo application
Based on businesses in MASTER_INDEX.csv
"""

import csv
import json
import random
from datetime import datetime, timedelta
from decimal import Decimal
import os

# Tax year to generate
TAX_YEAR = 2023

# Industry-specific profit margins and financial characteristics
INDUSTRY_PROFILES = {
    "Retail Bakery": {"margin": (0.05, 0.15), "cogs_pct": (0.35, 0.45), "labor_pct": (0.25, 0.35)},
    "Computer Repair Services": {"margin": (0.15, 0.25), "cogs_pct": (0.20, 0.30), "labor_pct": (0.20, 0.30)},
    "Landscaping Services": {"margin": (0.10, 0.20), "cogs_pct": (0.25, 0.35), "labor_pct": (0.30, 0.40)},
    "Restaurant": {"margin": (0.03, 0.10), "cogs_pct": (0.30, 0.35), "labor_pct": (0.30, 0.35)},
    "Auto Body Repair": {"margin": (0.15, 0.25), "cogs_pct": (0.25, 0.35), "labor_pct": (0.25, 0.30)},
    "Child Care Services": {"margin": (0.10, 0.20), "cogs_pct": (0.15, 0.25), "labor_pct": (0.40, 0.50)},
    "Fitness Center": {"margin": (0.15, 0.30), "cogs_pct": (0.10, 0.20), "labor_pct": (0.25, 0.35)},
    "Seafood Retail": {"margin": (0.08, 0.15), "cogs_pct": (0.45, 0.55), "labor_pct": (0.15, 0.25)},
    "Plumbing Services": {"margin": (0.20, 0.30), "cogs_pct": (0.20, 0.30), "labor_pct": (0.25, 0.35)},
    "Catering Services": {"margin": (0.10, 0.20), "cogs_pct": (0.30, 0.40), "labor_pct": (0.25, 0.35)},
    "Printing Services": {"margin": (0.15, 0.25), "cogs_pct": (0.30, 0.40), "labor_pct": (0.20, 0.30)},
    "Pet Grooming Services": {"margin": (0.20, 0.35), "cogs_pct": (0.10, 0.20), "labor_pct": (0.25, 0.35)},
    "HVAC Services": {"margin": (0.18, 0.28), "cogs_pct": (0.25, 0.35), "labor_pct": (0.25, 0.35)},
    "Yoga Studio": {"margin": (0.20, 0.35), "cogs_pct": (0.05, 0.15), "labor_pct": (0.30, 0.40)},
    "Furniture Repair": {"margin": (0.25, 0.40), "cogs_pct": (0.20, 0.30), "labor_pct": (0.20, 0.30)},
    "Laundry Services": {"margin": (0.15, 0.25), "cogs_pct": (0.10, 0.20), "labor_pct": (0.25, 0.35)},
    "Dental Laboratory": {"margin": (0.25, 0.40), "cogs_pct": (0.20, 0.30), "labor_pct": (0.25, 0.35)},
    "Coffee Shop": {"margin": (0.05, 0.15), "cogs_pct": (0.30, 0.40), "labor_pct": (0.25, 0.35)},
    "Security Services": {"margin": (0.10, 0.20), "cogs_pct": (0.15, 0.25), "labor_pct": (0.50, 0.60)},
    "Janitorial Services": {"margin": (0.08, 0.18), "cogs_pct": (0.15, 0.25), "labor_pct": (0.45, 0.55)},
}

def generate_revenue(years_in_business, loan_amount, creditworthiness):
    """Generate realistic annual revenue based on business characteristics"""
    # Base revenue on loan amount (typically 1-3x annual revenue)
    base_revenue = float(loan_amount.replace('$', '').replace(',', '')) * random.uniform(2.5, 4.5)

    # Adjust for years in business (growth factor)
    growth_factor = 1 + (years_in_business * random.uniform(0.03, 0.08))

    # Adjust for creditworthiness
    credit_multipliers = {
        'EXCELLENT': random.uniform(1.1, 1.3),
        'GOOD': random.uniform(0.95, 1.1),
        'OK': random.uniform(0.85, 1.0),
        'BAD': random.uniform(0.7, 0.9),
        'UGLY': random.uniform(0.5, 0.75)
    }

    revenue = base_revenue * growth_factor * credit_multipliers.get(creditworthiness, 1.0)
    return round(revenue, 2)

def generate_schedule_c(business_data, revenue):
    """Generate Schedule C (Profit or Loss from Business) for sole proprietors"""
    industry = business_data['Industry']
    profile = INDUSTRY_PROFILES.get(industry, INDUSTRY_PROFILES["Retail Bakery"])

    # Generate expenses based on industry profile
    cogs = revenue * random.uniform(*profile['cogs_pct'])
    labor = revenue * random.uniform(*profile['labor_pct'])

    # Other expenses
    rent = revenue * random.uniform(0.08, 0.15)
    utilities = revenue * random.uniform(0.02, 0.05)
    insurance = revenue * random.uniform(0.02, 0.04)
    repairs = revenue * random.uniform(0.01, 0.03)
    advertising = revenue * random.uniform(0.02, 0.05)
    supplies = revenue * random.uniform(0.01, 0.03)
    depreciation = revenue * random.uniform(0.02, 0.05)
    other_expenses = revenue * random.uniform(0.03, 0.06)

    total_expenses = (cogs + labor + rent + utilities + insurance +
                     repairs + advertising + supplies + depreciation + other_expenses)

    net_profit = revenue - total_expenses

    return {
        "form": "Schedule C",
        "tax_year": TAX_YEAR,
        "business_name": business_data['Business Name'],
        "ein": business_data['EIN'],
        "principal_business_code": business_data['SIC Code'],
        "business_address": {
            "state": business_data['State']
        },
        "accounting_method": "Cash",
        "material_participation": True,

        # Part I: Income
        "gross_receipts": round(revenue, 2),
        "returns_allowances": 0,
        "cost_of_goods_sold": round(cogs, 2),
        "gross_profit": round(revenue - cogs, 2),
        "other_income": 0,
        "gross_income": round(revenue - cogs, 2),

        # Part II: Expenses
        "expenses": {
            "advertising": round(advertising, 2),
            "car_truck": 0,
            "commissions_fees": 0,
            "contract_labor": round(labor * 0.3, 2),
            "depletion": 0,
            "depreciation": round(depreciation, 2),
            "employee_benefit_programs": round(labor * 0.05, 2),
            "insurance": round(insurance, 2),
            "interest_mortgage": 0,
            "interest_other": round(revenue * random.uniform(0.01, 0.03), 2),
            "legal_professional": round(revenue * random.uniform(0.005, 0.015), 2),
            "office_expense": round(supplies, 2),
            "pension_profit_sharing": 0,
            "rent_lease_vehicles": 0,
            "rent_lease_property": round(rent, 2),
            "repairs_maintenance": round(repairs, 2),
            "supplies": round(supplies * 0.5, 2),
            "taxes_licenses": round(revenue * random.uniform(0.01, 0.02), 2),
            "travel": round(revenue * random.uniform(0.005, 0.015), 2),
            "deductible_meals": round(revenue * random.uniform(0.01, 0.02), 2),
            "utilities": round(utilities, 2),
            "wages": round(labor * 0.65, 2),
            "other_expenses": round(other_expenses, 2)
        },

        "total_expenses": round(total_expenses, 2),
        "tentative_profit": round(net_profit, 2),
        "net_profit_loss": round(net_profit, 2)
    }

def generate_form_1040(business_data, schedule_c_data):
    """Generate Form 1040 (Individual Income Tax Return) for sole proprietor"""
    net_profit = schedule_c_data['net_profit_loss']

    # Owner information
    owner_name = business_data['Owner 1 Name']
    owner_ssn = business_data['Owner 1 SSN']

    # Additional income (interest, dividends, etc.)
    interest_income = random.uniform(500, 5000)
    dividend_income = random.uniform(1000, 10000)

    # Total income
    total_income = net_profit + interest_income + dividend_income

    # Adjusted Gross Income (AGI)
    self_employment_tax_deduction = net_profit * 0.0765  # Half of SE tax
    sep_ira_contribution = min(net_profit * 0.20, 66000)  # Simplified
    agi = total_income - self_employment_tax_deduction - sep_ira_contribution

    # Standard deduction for 2023
    standard_deduction = 13850 if business_data.get('Owner 2 Name') == '' else 27700

    # Taxable income
    taxable_income = max(0, agi - standard_deduction)

    # Federal income tax (simplified)
    federal_tax = calculate_federal_tax(taxable_income, business_data.get('Owner 2 Name') != '')

    # Self-employment tax
    se_tax = net_profit * 0.153 if net_profit > 0 else 0

    # Total tax
    total_tax = federal_tax + se_tax

    return {
        "form": "1040",
        "tax_year": TAX_YEAR,
        "filing_status": "Married Filing Jointly" if business_data.get('Owner 2 Name') else "Single",

        "taxpayer": {
            "name": owner_name,
            "ssn": owner_ssn,
            "address": {
                "state": business_data['State']
            }
        },

        "spouse": {
            "name": business_data.get('Owner 2 Name', ''),
            "ssn": business_data.get('Owner 2 SSN', '')
        } if business_data.get('Owner 2 Name') else None,

        # Income
        "wages_salaries": 0,
        "interest_income": round(interest_income, 2),
        "dividend_income": round(dividend_income, 2),
        "business_income": round(net_profit, 2),
        "capital_gains": 0,
        "other_income": 0,
        "total_income": round(total_income, 2),

        # Adjustments
        "self_employment_tax_deduction": round(self_employment_tax_deduction, 2),
        "sep_ira_deduction": round(sep_ira_contribution, 2),
        "health_insurance_deduction": round(random.uniform(5000, 15000), 2),
        "total_adjustments": round(self_employment_tax_deduction + sep_ira_contribution, 2),

        # AGI
        "adjusted_gross_income": round(agi, 2),

        # Deductions
        "standard_deduction": standard_deduction,
        "taxable_income": round(taxable_income, 2),

        # Tax
        "federal_income_tax": round(federal_tax, 2),
        "self_employment_tax": round(se_tax, 2),
        "total_tax": round(total_tax, 2),

        # Payments
        "federal_withholding": 0,
        "estimated_tax_payments": round(total_tax * random.uniform(0.8, 1.1), 2),

        # Refund or Amount Owed
        "refund_or_owed": round((total_tax * random.uniform(0.8, 1.1)) - total_tax, 2)
    }

def generate_form_1120s(business_data, revenue):
    """Generate Form 1120-S (S-Corporation Income Tax Return)"""
    industry = business_data['Industry']
    profile = INDUSTRY_PROFILES.get(industry, INDUSTRY_PROFILES["Retail Bakery"])

    # Generate income and expenses
    cogs = revenue * random.uniform(*profile['cogs_pct'])
    gross_profit = revenue - cogs

    # Operating expenses
    salaries_wages = revenue * random.uniform(*profile['labor_pct'])
    rent = revenue * random.uniform(0.08, 0.15)
    utilities = revenue * random.uniform(0.02, 0.05)
    insurance = revenue * random.uniform(0.02, 0.04)
    depreciation = revenue * random.uniform(0.02, 0.05)
    advertising = revenue * random.uniform(0.02, 0.05)
    office_expenses = revenue * random.uniform(0.01, 0.03)
    other_expenses = revenue * random.uniform(0.03, 0.06)

    total_expenses = (salaries_wages + rent + utilities + insurance +
                     depreciation + advertising + office_expenses + other_expenses)

    ordinary_income = gross_profit - total_expenses

    # Balance sheet
    cash = revenue * random.uniform(0.05, 0.15)
    accounts_receivable = revenue * random.uniform(0.08, 0.15)
    inventory = cogs * random.uniform(0.10, 0.20)
    other_current_assets = revenue * random.uniform(0.02, 0.05)
    fixed_assets = revenue * random.uniform(0.30, 0.50)
    accumulated_depreciation = fixed_assets * random.uniform(0.20, 0.40)

    total_assets = (cash + accounts_receivable + inventory +
                   other_current_assets + fixed_assets - accumulated_depreciation)

    accounts_payable = revenue * random.uniform(0.05, 0.10)
    current_portion_ltd = float(business_data['Loan Amount'].replace('$', '').replace(',', '')) * 0.10
    other_current_liabilities = revenue * random.uniform(0.02, 0.05)
    long_term_debt = float(business_data['Loan Amount'].replace('$', '').replace(',', '')) * 0.90

    total_liabilities = (accounts_payable + current_portion_ltd +
                        other_current_liabilities + long_term_debt)

    capital_stock = 1000  # Nominal
    retained_earnings = total_assets - total_liabilities - capital_stock

    return {
        "form": "1120-S",
        "tax_year": TAX_YEAR,
        "corporation_name": business_data['Business Name'],
        "ein": business_data['EIN'],
        "business_code": business_data['SIC Code'],
        "date_incorporated": f"{business_data['Formation Year']}-01-01",
        "state_of_incorporation": business_data['State'],

        # Income
        "gross_receipts": round(revenue, 2),
        "returns_allowances": 0,
        "cost_of_goods_sold": round(cogs, 2),
        "gross_profit": round(gross_profit, 2),
        "net_gain_loss": 0,
        "other_income": 0,
        "total_income": round(gross_profit, 2),

        # Deductions
        "compensation_officers": round(salaries_wages * 0.30, 2),
        "salaries_wages": round(salaries_wages * 0.70, 2),
        "repairs_maintenance": round(revenue * random.uniform(0.01, 0.03), 2),
        "bad_debts": round(revenue * random.uniform(0.001, 0.01), 2),
        "rents": round(rent, 2),
        "taxes_licenses": round(revenue * random.uniform(0.01, 0.02), 2),
        "interest": round(long_term_debt * random.uniform(0.05, 0.08), 2),
        "depreciation": round(depreciation, 2),
        "advertising": round(advertising, 2),
        "pension_plans": round(salaries_wages * random.uniform(0.03, 0.06), 2),
        "employee_benefits": round(salaries_wages * random.uniform(0.05, 0.10), 2),
        "other_deductions": round(other_expenses, 2),
        "total_deductions": round(total_expenses, 2),

        "ordinary_business_income": round(ordinary_income, 2),

        # Schedule K - Shareholders' shares
        "schedule_k": {
            "ordinary_income": round(ordinary_income, 2),
            "rental_real_estate_income": 0,
            "other_rental_income": 0,
            "interest_income": round(random.uniform(500, 2000), 2),
            "dividends": 0,
            "royalties": 0,
            "net_short_term_capital_gain": 0,
            "net_long_term_capital_gain": 0,
            "other_income": 0
        },

        # Balance Sheet
        "balance_sheet": {
            "beginning_of_year": {
                "assets": {
                    "cash": round(cash * 0.90, 2),
                    "accounts_receivable": round(accounts_receivable * 0.90, 2),
                    "inventory": round(inventory * 0.90, 2),
                    "other_current_assets": round(other_current_assets * 0.90, 2),
                    "fixed_assets": round(fixed_assets, 2),
                    "accumulated_depreciation": round(accumulated_depreciation * 0.75, 2),
                    "other_assets": 0,
                    "total_assets": round(total_assets * 0.90, 2)
                },
                "liabilities_equity": {
                    "accounts_payable": round(accounts_payable * 0.90, 2),
                    "current_portion_long_term_debt": round(current_portion_ltd, 2),
                    "other_current_liabilities": round(other_current_liabilities * 0.90, 2),
                    "long_term_debt": round(long_term_debt * 1.10, 2),
                    "capital_stock": capital_stock,
                    "retained_earnings": round((total_assets * 0.90) - (accounts_payable * 0.90) - current_portion_ltd - (other_current_liabilities * 0.90) - (long_term_debt * 1.10) - capital_stock, 2),
                    "total_liabilities_equity": round(total_assets * 0.90, 2)
                }
            },
            "end_of_year": {
                "assets": {
                    "cash": round(cash, 2),
                    "accounts_receivable": round(accounts_receivable, 2),
                    "inventory": round(inventory, 2),
                    "other_current_assets": round(other_current_assets, 2),
                    "fixed_assets": round(fixed_assets, 2),
                    "accumulated_depreciation": round(accumulated_depreciation, 2),
                    "other_assets": 0,
                    "total_assets": round(total_assets, 2)
                },
                "liabilities_equity": {
                    "accounts_payable": round(accounts_payable, 2),
                    "current_portion_long_term_debt": round(current_portion_ltd, 2),
                    "other_current_liabilities": round(other_current_liabilities, 2),
                    "long_term_debt": round(long_term_debt, 2),
                    "capital_stock": capital_stock,
                    "retained_earnings": round(retained_earnings, 2),
                    "total_liabilities_equity": round(total_assets, 2)
                }
            }
        }
    }

def generate_form_1065(business_data, revenue):
    """Generate Form 1065 (Partnership Return) for LLCs"""
    industry = business_data['Industry']
    profile = INDUSTRY_PROFILES.get(industry, INDUSTRY_PROFILES["Retail Bakery"])

    # Similar structure to 1120-S
    cogs = revenue * random.uniform(*profile['cogs_pct'])
    gross_profit = revenue - cogs

    # Operating expenses
    salaries_wages = revenue * random.uniform(*profile['labor_pct'])
    guaranteed_payments = salaries_wages * 0.40  # Partner payments
    rent = revenue * random.uniform(0.08, 0.15)
    utilities = revenue * random.uniform(0.02, 0.05)
    insurance = revenue * random.uniform(0.02, 0.04)
    depreciation = revenue * random.uniform(0.02, 0.05)
    advertising = revenue * random.uniform(0.02, 0.05)
    other_expenses = revenue * random.uniform(0.05, 0.10)

    total_expenses = (salaries_wages + guaranteed_payments + rent + utilities +
                     insurance + depreciation + advertising + other_expenses)

    ordinary_income = gross_profit - total_expenses

    return {
        "form": "1065",
        "tax_year": TAX_YEAR,
        "partnership_name": business_data['Business Name'],
        "ein": business_data['EIN'],
        "business_code": business_data['SIC Code'],
        "date_business_started": f"{business_data['Formation Year']}-01-01",

        # Income
        "gross_receipts": round(revenue, 2),
        "returns_allowances": 0,
        "cost_of_goods_sold": round(cogs, 2),
        "gross_profit": round(gross_profit, 2),
        "other_income": 0,
        "total_income": round(gross_profit, 2),

        # Deductions
        "salaries_wages": round(salaries_wages, 2),
        "guaranteed_payments": round(guaranteed_payments, 2),
        "repairs_maintenance": round(revenue * random.uniform(0.01, 0.03), 2),
        "bad_debts": round(revenue * random.uniform(0.001, 0.01), 2),
        "rent": round(rent, 2),
        "taxes_licenses": round(revenue * random.uniform(0.01, 0.02), 2),
        "interest": round(revenue * random.uniform(0.02, 0.04), 2),
        "depreciation": round(depreciation, 2),
        "advertising": round(advertising, 2),
        "other_deductions": round(other_expenses, 2),
        "total_deductions": round(total_expenses, 2),

        "ordinary_income": round(ordinary_income, 2),

        # Schedule K
        "schedule_k": {
            "ordinary_income": round(ordinary_income, 2),
            "guaranteed_payments": round(guaranteed_payments, 2),
            "interest_income": round(random.uniform(500, 2000), 2)
        }
    }

def generate_schedule_k1_1120s(business_data, form_1120s, owner_num=1):
    """Generate Schedule K-1 for S-Corporation shareholder"""
    ownership_pct = float(business_data[f'Owner {owner_num} Ownership %'].replace('%', '')) / 100
    ordinary_income = form_1120s['ordinary_business_income'] * ownership_pct

    return {
        "form": "Schedule K-1 (Form 1120-S)",
        "tax_year": TAX_YEAR,
        "corporation_name": business_data['Business Name'],
        "corporation_ein": business_data['EIN'],

        "shareholder": {
            "name": business_data[f'Owner {owner_num} Name'],
            "ssn": business_data[f'Owner {owner_num} SSN'],
            "ownership_percentage": ownership_pct * 100
        },

        "shareholder_share_of_income": {
            "ordinary_business_income": round(ordinary_income, 2),
            "net_rental_real_estate_income": 0,
            "other_net_rental_income": 0,
            "interest_income": round(form_1120s['schedule_k']['interest_income'] * ownership_pct, 2),
            "dividends": 0,
            "royalties": 0,
            "net_short_term_capital_gain": 0,
            "net_long_term_capital_gain": 0
        },

        "shareholder_share_of_deductions": {
            "section_179_deduction": 0,
            "charitable_contributions": 0,
            "investment_interest": 0
        },

        "shareholder_capital_account": {
            "beginning_capital": round(form_1120s['balance_sheet']['beginning_of_year']['liabilities_equity']['retained_earnings'] * ownership_pct, 2),
            "capital_contributed": 0,
            "current_year_income": round(ordinary_income, 2),
            "withdrawals_distributions": round(ordinary_income * random.uniform(0.3, 0.6), 2),
            "ending_capital": round(form_1120s['balance_sheet']['end_of_year']['liabilities_equity']['retained_earnings'] * ownership_pct, 2)
        }
    }

def calculate_federal_tax(taxable_income, married):
    """Calculate federal income tax using 2023 tax brackets"""
    if married:
        brackets = [
            (22000, 0.10),
            (89075, 0.12),
            (190750, 0.22),
            (364200, 0.24),
            (462500, 0.32),
            (693750, 0.35),
            (float('inf'), 0.37)
        ]
    else:
        brackets = [
            (11000, 0.10),
            (44725, 0.12),
            (95375, 0.22),
            (182100, 0.24),
            (231250, 0.32),
            (578125, 0.35),
            (float('inf'), 0.37)
        ]

    tax = 0
    previous_bracket = 0

    for bracket_limit, rate in brackets:
        if taxable_income <= bracket_limit:
            tax += (taxable_income - previous_bracket) * rate
            break
        else:
            tax += (bracket_limit - previous_bracket) * rate
            previous_bracket = bracket_limit

    return tax

def main():
    """Main function to generate all tax data"""
    # Read MASTER_INDEX.csv
    master_index_path = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'MASTER_INDEX.csv')

    with open(master_index_path, 'r') as f:
        reader = csv.DictReader(f)
        businesses = list(reader)

    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), 'tax_returns_data')
    os.makedirs(output_dir, exist_ok=True)

    # Generate tax returns for each business
    for business in businesses:
        if not business.get('Business Name'):
            continue

        print(f"\nGenerating tax returns for {business['Business Name']}...")

        # Generate revenue
        revenue = generate_revenue(
            int(business['Years in Business']),
            business['Loan Amount'],
            business['Creditworthiness']
        )

        tax_data = {
            "business_info": business,
            "tax_year": TAX_YEAR,
            "annual_revenue": revenue
        }

        # Generate appropriate forms based on entity type
        entity_type = business['Entity Type']

        if entity_type == 'Sole Proprietorship':
            schedule_c = generate_schedule_c(business, revenue)
            form_1040 = generate_form_1040(business, schedule_c)

            tax_data['forms'] = {
                "form_1040": form_1040,
                "schedule_c": schedule_c
            }

        elif entity_type == 'S-Corp':
            form_1120s = generate_form_1120s(business, revenue)
            k1_owner1 = generate_schedule_k1_1120s(business, form_1120s, 1)

            tax_data['forms'] = {
                "form_1120s": form_1120s,
                "schedule_k1_owner1": k1_owner1
            }

            # Add second owner K-1 if applicable
            if business.get('Owner 2 Name'):
                k1_owner2 = generate_schedule_k1_1120s(business, form_1120s, 2)
                tax_data['forms']['schedule_k1_owner2'] = k1_owner2

        elif entity_type == 'LLC':
            form_1065 = generate_form_1065(business, revenue)

            tax_data['forms'] = {
                "form_1065": form_1065
            }

        # Save to JSON file
        folder_name = business.get('Folder Name', business['Business Name'].lower().replace(' ', '_'))
        output_file = os.path.join(output_dir, f"{folder_name}_tax_return_{TAX_YEAR}.json")

        with open(output_file, 'w') as f:
            json.dump(tax_data, f, indent=2)

        print(f"  ✓ Generated tax return: {output_file}")
        print(f"    Revenue: ${revenue:,.2f}")
        print(f"    Entity Type: {entity_type}")

    print(f"\n✅ Tax return generation complete!")
    print(f"   Output directory: {output_dir}")
    print(f"   Total files generated: {len([b for b in businesses if b.get('Business Name')])}")

if __name__ == "__main__":
    main()
