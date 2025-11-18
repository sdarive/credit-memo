# IRS Tax Return Data - Test Data Package

## Overview

This package contains **realistic, synthetic IRS tax return data** for 20 small businesses, generated to test and demonstrate the credit memo application's ability to extract financial information from tax documents.

**Generation Date:** November 2024
**Tax Year:** 2023
**Number of Businesses:** 20
**Total Tax Documents:** 43 forms (1040s, 1120-S, Schedule Cs, K-1s)

---

## 📁 Directory Structure

```
backend/
├── tax_returns_data/          # JSON data files (structured)
│   └── *.json                 # 20 tax return files in JSON format
├── tax_returns_formatted/     # Text-formatted IRS forms
│   ├── *_Form_1040.txt       # Individual tax returns
│   ├── *_Schedule_C.txt      # Business profit/loss schedules
│   ├── *_Form_1120S.txt      # S-Corporation returns
│   └── *_Schedule_K1_*.txt   # Shareholder K-1 forms
├── generate_irs_tax_data.py   # Data generation script
└── format_tax_forms.py        # Form formatting script
```

---

## 📋 What Was Generated

### By Entity Type

| Entity Type         | Count | Forms Generated                          |
|---------------------|-------|------------------------------------------|
| Sole Proprietorship | 7     | Form 1040, Schedule C                    |
| S-Corporation       | 10    | Form 1120-S, Schedule K-1 (per owner)    |
| LLC                 | 3     | Form 1065 (Partnership Return)           |
| **TOTAL**           | **20**| **43 tax documents**                     |

### By Industry

The tax returns cover diverse industries including:
- 🍰 Retail Bakery
- 💻 Computer Repair Services
- 🌿 Landscaping Services
- 🍽️ Restaurant
- 🚗 Auto Body Repair
- 👶 Child Care Services
- 💪 Fitness Center
- 🐟 Seafood Retail
- 🔧 Plumbing Services
- 🎉 Catering Services
- 📄 Printing Services
- 🐾 Pet Grooming
- 🌡️ HVAC Services
- 🧘 Yoga Studio
- 🪑 Furniture Repair
- 🧺 Laundromat
- 🦷 Dental Laboratory
- ☕ Coffee Shop
- 🔒 Security Services
- 🧹 Janitorial Services

---

## 📊 Sample Business Examples

### Example 1: AutoCare Collision Center (Sole Proprietor)
- **Owner:** Michael Thompson
- **Industry:** Auto Body Repair
- **Revenue:** $2,279,728
- **Net Profit:** $42,885
- **Forms:** Form 1040, Schedule C
- **Creditworthiness:** EXCELLENT

### Example 2: Precision Dental Lab Inc (S-Corporation)
- **Owners:** Dr. Steven Kim (65%), Dr. Linda Park (35%)
- **Industry:** Dental Laboratory
- **Revenue:** $3,876,804
- **Ordinary Income:** ~$600,000 (varies)
- **Forms:** Form 1120-S, 2 Schedule K-1s
- **Creditworthiness:** EXCELLENT

### Example 3: Sunrise Bakery LLC (Partnership)
- **Owners:** Maria Rodriguez (60%), Carlos Martinez (40%)
- **Industry:** Retail Bakery
- **Revenue:** $1,690,136
- **Forms:** Form 1065, Schedule K-1s
- **Creditworthiness:** EXCELLENT

---

## 🧮 Financial Data Included

Each tax return contains realistic financial data based on industry-specific characteristics:

### Income Statement Data
- ✅ Gross receipts/sales
- ✅ Cost of goods sold (COGS)
- ✅ Gross profit
- ✅ Operating expenses (20+ categories)
- ✅ Net income/ordinary business income

### Balance Sheet Data (1120-S only)
- ✅ Assets: Cash, A/R, Inventory, Fixed Assets
- ✅ Liabilities: A/P, Current & Long-term Debt
- ✅ Equity: Capital Stock, Retained Earnings

### Tax Calculations
- ✅ Federal income tax
- ✅ Self-employment tax (1040)
- ✅ Deductions and adjustments
- ✅ Refunds or amounts owed

---

## 🎯 Use Cases for Credit Memo Application

### 1. **Document Upload Testing**
Upload the formatted `.txt` files to test the LandingAI ADE extraction:
```bash
# Example files to test:
- autocare_collision_center_tax_return_2023_Schedule_C.txt
- precision_dental_lab_inc_tax_return_2023_Form_1120S.txt
```

### 2. **Financial Ratio Extraction**
The application should extract key metrics for credit analysis:
- **Revenue** → Total Income / Gross Receipts
- **COGS** → Cost of Goods Sold
- **Operating Expenses** → Total Deductions
- **Net Income** → Net Profit / Ordinary Business Income
- **Assets/Liabilities** → Balance Sheet (1120-S)

### 3. **Credit Memo Generation**
Use extracted data to generate credit memos with:
- Historical financial performance analysis
- Debt service coverage calculations
- Profitability metrics
- Industry comparisons

### 4. **Multi-Year Analysis**
The data represents FY 2023. You can:
- Generate additional years with the scripts
- Test year-over-year trend analysis
- Validate growth projections

---

## 🛠️ Regenerating or Customizing Data

### Generate New Tax Returns

```bash
cd backend
python generate_irs_tax_data.py
```

This will create 20 JSON files in `tax_returns_data/` with randomized (but realistic) financial data.

### Format as IRS Forms

```bash
cd backend
python format_tax_forms.py
```

This converts JSON data into formatted text files that resemble actual IRS forms.

### Customize Industries or Revenue

Edit `generate_irs_tax_data.py`:

```python
# Adjust revenue generation
def generate_revenue(years_in_business, loan_amount, creditworthiness):
    base_revenue = float(loan_amount.replace('$', '').replace(',', '')) * 3.5  # Change multiplier
    # ... rest of logic

# Add new industries
INDUSTRY_PROFILES = {
    "Your Industry": {"margin": (0.10, 0.20), "cogs_pct": (0.30, 0.40), "labor_pct": (0.25, 0.35)},
    # ...
}
```

---

## 📈 Key Financial Metrics by Credit Rating

The generator creates realistic variations based on creditworthiness:

| Credit Rating | Revenue Multiplier | Profit Margin Range |
|---------------|-------------------|---------------------|
| EXCELLENT     | 1.1 - 1.3x        | 15-30%              |
| GOOD          | 0.95 - 1.1x       | 10-20%              |
| OK            | 0.85 - 1.0x       | 5-15%               |
| BAD           | 0.7 - 0.9x        | 0-10%               |
| UGLY          | 0.5 - 0.75x       | -5% to 5%           |

---

## 🔍 Data Accuracy & Realism

### Industry-Specific Modeling
- **COGS %**: Varies by industry (e.g., Seafood: 45-55%, Yoga: 5-15%)
- **Labor %**: Service industries higher (40-60% for janitorial/childcare)
- **Profit Margins**: Aligned with real-world industry benchmarks

### Tax Compliance
- **2023 Tax Brackets**: Accurate federal tax calculations
- **Standard Deductions**: $13,850 (single), $27,700 (married)
- **Self-Employment Tax**: 15.3% on net profit
- **Balance Sheets**: Beginning and end-of-year positions

### Realistic Business Characteristics
- **Revenue Growth**: Based on years in business (3-8% annually)
- **Debt Levels**: Tied to loan amounts from MASTER_INDEX.csv
- **Working Capital**: Appropriate current ratios for industries
- **Owner Distributions**: K-1 distributions at 30-60% of income

---

## 🚀 Quick Start Guide

### Step 1: Choose a Test Business
```bash
cd backend/tax_returns_formatted
ls *_Form_1040.txt  # Sole proprietorships
ls *_Form_1120S.txt # S-Corporations
```

### Step 2: Upload to Credit Memo App
1. Start the application (see main README.md)
2. Navigate to document upload
3. Upload a tax form (e.g., `autocare_collision_center_tax_return_2023_Schedule_C.txt`)
4. Review extracted financial data

### Step 3: Generate Credit Memo
- Review auto-extracted revenue, expenses, profit
- Check calculated financial ratios (DSCR, Current Ratio, etc.)
- Generate AI-powered credit memo narrative

---

## 📊 Sample Output - Schedule C

```
================================================================================
                        SCHEDULE C
                (Form 1040)
         Profit or Loss From Business
         (Sole Proprietorship)
================================================================================

Name of proprietor: Michael Thompson
Social Security Number: 130-95-7079

A.  Principal business or profession: Auto Body Repair
B.  Business name: AutoCare Collision Center
D.  Employer ID number (EIN): 59-9839976

1.  Gross receipts or sales                            $2,279,728.01
4.  Cost of goods sold                                 $718,137.27
5.  Gross profit                                       $1,561,590.74

28. Total expenses                                     $2,236,843.46

31. NET PROFIT OR (LOSS)                               $42,884.55
```

---

## 🔐 Data Privacy & Compliance

### Synthetic Data Only
- ✅ All data is **computer-generated and fictional**
- ✅ SSNs follow valid format but are randomized
- ✅ EINs follow valid format but are randomized
- ✅ Names, addresses, and business details are fictional
- ✅ **No real taxpayer information** is included

### Safe for Testing
- Can be shared publicly without privacy concerns
- Suitable for demos, hackathons, and development
- Complies with data protection regulations

---

## 📚 Additional Resources

### IRS Form References
- [Form 1040 Instructions](https://www.irs.gov/forms-pubs/about-form-1040)
- [Schedule C Instructions](https://www.irs.gov/forms-pubs/about-schedule-c-form-1040)
- [Form 1120-S Instructions](https://www.irs.gov/forms-pubs/about-form-1120-s)
- [Schedule K-1 Instructions](https://www.irs.gov/forms-pubs/about-schedule-k-1-form-1120-s)

### Industry Benchmarks
- [BizStats Industry Financial Ratios](https://www.bizstats.com/)
- [RMA Annual Statement Studies](https://rmahq.org/)
- [IRS Industry Audit Guides](https://www.irs.gov/businesses/small-businesses-self-employed/market-segment-specialization-program-mssp)

---

## 🐛 Troubleshooting

### Issue: JSON files not generating
**Solution:** Check that `datasets/MASTER_INDEX.csv` exists and has valid data.

### Issue: Formatted text files missing
**Solution:** Run `python format_tax_forms.py` after generating JSON data.

### Issue: Unrealistic financial ratios
**Solution:** Adjust `INDUSTRY_PROFILES` in `generate_irs_tax_data.py` to match your target metrics.

---

## 📝 File Naming Convention

```
{business_folder_name}_tax_return_{year}_{form_type}.{ext}

Examples:
- autocare_collision_center_tax_return_2023.json          # Raw data
- autocare_collision_center_tax_return_2023_Form_1040.txt # Formatted
- autocare_collision_center_tax_return_2023_Schedule_C.txt
- precision_dental_lab_inc_tax_return_2023_Form_1120S.txt
- precision_dental_lab_inc_tax_return_2023_Schedule_K1_Owner1.txt
```

---

## ✅ Data Validation Checklist

Before using tax data in production testing:

- [ ] Revenue figures are realistic for business size
- [ ] Profit margins align with industry benchmarks
- [ ] Balance sheets balance (Assets = Liabilities + Equity)
- [ ] Tax calculations are accurate for 2023 tax year
- [ ] K-1 ownership percentages match MASTER_INDEX.csv
- [ ] Expense categories are appropriate for industry
- [ ] All SSNs and EINs follow valid format patterns

---

## 🎉 Summary

**You now have 20 realistic tax returns covering:**
- ✅ 7 Sole Proprietorships (Form 1040, Schedule C)
- ✅ 10 S-Corporations (Form 1120-S, Schedule K-1s)
- ✅ 3 LLCs (Form 1065)
- ✅ 20 different industries
- ✅ Revenue from $467K to $3.9M
- ✅ Complete financial statements
- ✅ Formatted text files ready for upload

**Use these to test:**
1. Document extraction (LandingAI ADE)
2. Financial ratio calculations
3. Credit memo generation
4. Multi-document analysis
5. RAG-enhanced narrative generation

---

## 📧 Questions or Issues?

If you encounter any problems or have questions about the tax data:
1. Check the troubleshooting section above
2. Review the generation scripts in `backend/`
3. Refer to the main project README.md

---

**Generated by:** IRS Tax Data Generator v1.0
**For:** LandingAI Financial AI Hackathon 2025
**Project:** Ernie - AI Credit Assistant

---

*Note: This is synthetic test data for software development and demonstration purposes only. Not intended for submission to tax authorities.*
