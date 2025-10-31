"""
Financial Calculations Module
Calculates key lending ratios for credit analysis
"""

from typing import Dict, Any, Optional


class FinancialCalculator:
    """Calculator for financial ratios used in credit analysis"""

    @staticmethod
    def calculate_dscr(
        net_operating_income: Optional[float],
        total_debt_service: Optional[float]
    ) -> Optional[float]:
        """
        Calculate Debt Service Coverage Ratio (DSCR)

        DSCR = Net Operating Income / Total Debt Service

        A DSCR > 1.0 indicates the entity generates sufficient income to cover debt payments
        Typical minimum for lending: 1.20 - 1.25

        Args:
            net_operating_income: Net operating income or EBITDA
            total_debt_service: Annual debt service (principal + interest)

        Returns:
            DSCR ratio or None if calculation not possible
        """
        if net_operating_income is None or total_debt_service is None:
            return None

        if total_debt_service == 0:
            return None

        return round(net_operating_income / total_debt_service, 2)

    @staticmethod
    def calculate_leverage_ratio(
        total_debt: Optional[float],
        total_assets: Optional[float]
    ) -> Optional[float]:
        """
        Calculate Leverage Ratio (Debt-to-Assets)

        Leverage Ratio = Total Debt / Total Assets

        Measures the proportion of assets financed by debt
        Lower is generally better (less leveraged)

        Args:
            total_debt: Total outstanding debt
            total_assets: Total assets

        Returns:
            Leverage ratio or None if calculation not possible
        """
        if total_debt is None or total_assets is None:
            return None

        if total_assets == 0:
            return None

        return round(total_debt / total_assets, 2)

    @staticmethod
    def calculate_debt_to_equity(
        total_debt: Optional[float],
        total_equity: Optional[float]
    ) -> Optional[float]:
        """
        Calculate Debt-to-Equity Ratio

        D/E Ratio = Total Debt / Total Equity

        Args:
            total_debt: Total outstanding debt
            total_equity: Total shareholder equity

        Returns:
            Debt-to-equity ratio or None if calculation not possible
        """
        if total_debt is None or total_equity is None:
            return None

        if total_equity == 0:
            return None

        return round(total_debt / total_equity, 2)

    @staticmethod
    def calculate_current_ratio(
        current_assets: Optional[float],
        current_liabilities: Optional[float]
    ) -> Optional[float]:
        """
        Calculate Current Ratio (Liquidity measure)

        Current Ratio = Current Assets / Current Liabilities

        Measures ability to pay short-term obligations
        Typical healthy range: 1.5 - 3.0

        Args:
            current_assets: Current assets (cash, receivables, inventory)
            current_liabilities: Current liabilities (due within 1 year)

        Returns:
            Current ratio or None if calculation not possible
        """
        if current_assets is None or current_liabilities is None:
            return None

        if current_liabilities == 0:
            return None

        return round(current_assets / current_liabilities, 2)

    @staticmethod
    def calculate_quick_ratio(
        current_assets: Optional[float],
        inventory: Optional[float],
        current_liabilities: Optional[float]
    ) -> Optional[float]:
        """
        Calculate Quick Ratio (Acid-Test Ratio)

        Quick Ratio = (Current Assets - Inventory) / Current Liabilities

        More conservative liquidity measure than current ratio
        Typical healthy minimum: 1.0

        Args:
            current_assets: Current assets
            inventory: Inventory value
            current_liabilities: Current liabilities

        Returns:
            Quick ratio or None if calculation not possible
        """
        if current_assets is None or current_liabilities is None:
            return None

        if current_liabilities == 0:
            return None

        inventory = inventory or 0
        quick_assets = current_assets - inventory

        return round(quick_assets / current_liabilities, 2)

    @staticmethod
    def calculate_roa(
        net_income: Optional[float],
        total_assets: Optional[float]
    ) -> Optional[float]:
        """
        Calculate Return on Assets (ROA)

        ROA = Net Income / Total Assets

        Measures how efficiently assets generate profit
        Expressed as percentage

        Args:
            net_income: Net income
            total_assets: Total assets

        Returns:
            ROA as percentage or None if calculation not possible
        """
        if net_income is None or total_assets is None:
            return None

        if total_assets == 0:
            return None

        return round((net_income / total_assets) * 100, 2)

    @staticmethod
    def calculate_roe(
        net_income: Optional[float],
        total_equity: Optional[float]
    ) -> Optional[float]:
        """
        Calculate Return on Equity (ROE)

        ROE = Net Income / Total Equity

        Measures return generated on shareholders' equity
        Expressed as percentage

        Args:
            net_income: Net income
            total_equity: Total shareholder equity

        Returns:
            ROE as percentage or None if calculation not possible
        """
        if net_income is None or total_equity is None:
            return None

        if total_equity == 0:
            return None

        return round((net_income / total_equity) * 100, 2)

    @staticmethod
    def calculate_debt_to_ebitda(
        total_debt: Optional[float],
        ebitda: Optional[float]
    ) -> Optional[float]:
        """
        Calculate Total Debt to EBITDA

        Total Debt to EBITDA = Total Debt / EBITDA

        Assesses leverage and repayment capacity
        Lower is better; typical healthy range: < 3.0

        Args:
            total_debt: Total outstanding debt
            ebitda: Earnings Before Interest, Taxes, Depreciation, and Amortization

        Returns:
            Debt to EBITDA ratio or None if calculation not possible
        """
        if total_debt is None or ebitda is None:
            return None

        if ebitda == 0:
            return None

        return round(total_debt / ebitda, 2)

    @staticmethod
    def calculate_net_income_margin(
        net_income: Optional[float],
        sales: Optional[float]
    ) -> Optional[float]:
        """
        Calculate Net Income Margin

        Net Income Margin = Net Income / Sales

        Assesses profitability
        Expressed as percentage

        Args:
            net_income: Net income
            sales: Total sales/revenue

        Returns:
            Net income margin as percentage or None if calculation not possible
        """
        if net_income is None or sales is None:
            return None

        if sales == 0:
            return None

        return round((net_income / sales) * 100, 2)

    @staticmethod
    def calculate_interest_coverage(
        ebit: Optional[float],
        interest_expense: Optional[float]
    ) -> Optional[float]:
        """
        Calculate Interest Coverage Ratio

        Interest Coverage Ratio = EBIT / Interest Expense

        Tests ability to pay interest on debt
        Higher is better; typical minimum: 2.0

        Args:
            ebit: Earnings Before Interest and Taxes
            interest_expense: Annual interest expense

        Returns:
            Interest coverage ratio or None if calculation not possible
        """
        if ebit is None or interest_expense is None:
            return None

        if interest_expense == 0:
            return None

        return round(ebit / interest_expense, 2)

    @staticmethod
    def calculate_working_capital(
        current_assets: Optional[float],
        current_liabilities: Optional[float]
    ) -> Optional[float]:
        """
        Calculate Working Capital

        Working Capital = Current Assets - Current Liabilities

        Indicates liquidity for daily operations
        Positive is good

        Args:
            current_assets: Current assets
            current_liabilities: Current liabilities

        Returns:
            Working capital or None if calculation not possible
        """
        if current_assets is None or current_liabilities is None:
            return None

        return round(current_assets - current_liabilities, 2)

    @staticmethod
    def calculate_dso(
        accounts_receivable: Optional[float],
        total_credit_sales: Optional[float],
        num_days: int = 365
    ) -> Optional[float]:
        """
        Calculate Days Sales Outstanding (DSO)

        DSO = (Accounts Receivable / Total Credit Sales) * Number of Days

        Measures efficiency in collecting receivables
        Lower is better

        Args:
            accounts_receivable: Accounts receivable balance
            total_credit_sales: Total credit sales (or revenue)
            num_days: Number of days in period (default 365)

        Returns:
            DSO in days or None if calculation not possible
        """
        if accounts_receivable is None or total_credit_sales is None:
            return None

        if total_credit_sales == 0:
            return None

        return round((accounts_receivable / total_credit_sales) * num_days, 2)

    def calculate_all_ratios(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate all available ratios from financial data

        Args:
            financial_data: Dictionary containing financial metrics

        Returns:
            Dictionary with calculated ratios (all 9 key ratios for credit analysis)
        """
        ratios = {
            # 1. DSCR
            'dscr': self.calculate_dscr(
                financial_data.get('operating_income'),
                financial_data.get('debt_service')
            ),
            # 2. Total Debt to EBITDA
            'debt_to_ebitda': self.calculate_debt_to_ebitda(
                financial_data.get('total_debt'),
                financial_data.get('ebitda')
            ),
            # 3. Current Ratio
            'current_ratio': self.calculate_current_ratio(
                financial_data.get('current_assets'),
                financial_data.get('current_liabilities')
            ),
            # 4. Quick Ratio
            'quick_ratio': self.calculate_quick_ratio(
                financial_data.get('current_assets'),
                financial_data.get('inventory'),
                financial_data.get('current_liabilities')
            ),
            # 5. Net Income Margin
            'net_income_margin': self.calculate_net_income_margin(
                financial_data.get('net_income'),
                financial_data.get('revenue')
            ),
            # 6. Interest Coverage Ratio
            'interest_coverage': self.calculate_interest_coverage(
                financial_data.get('ebit'),
                financial_data.get('interest_expense')
            ),
            # 7. Leverage Ratio
            'leverage_ratio': self.calculate_leverage_ratio(
                financial_data.get('total_debt'),
                financial_data.get('total_assets')
            ),
            # 8. Working Capital
            'working_capital': self.calculate_working_capital(
                financial_data.get('current_assets'),
                financial_data.get('current_liabilities')
            ),
            # 9. Days Sales Outstanding
            'dso': self.calculate_dso(
                financial_data.get('accounts_receivable'),
                financial_data.get('revenue')
            ),
            # Additional useful ratios
            'debt_to_equity': self.calculate_debt_to_equity(
                financial_data.get('total_debt'),
                financial_data.get('total_equity')
            ),
            'roa': self.calculate_roa(
                financial_data.get('net_income'),
                financial_data.get('total_assets')
            ),
            'roe': self.calculate_roe(
                financial_data.get('net_income'),
                financial_data.get('total_equity')
            )
        }

        # Add interpretations
        ratios['interpretations'] = self._interpret_ratios(ratios)

        return ratios

    def _interpret_ratios(self, ratios: Dict[str, Any]) -> Dict[str, str]:
        """
        Provide interpretations for calculated ratios

        Args:
            ratios: Dictionary of calculated ratios

        Returns:
            Dictionary with interpretations
        """
        interpretations = {}

        # 1. DSCR interpretation
        dscr = ratios.get('dscr')
        if dscr is not None:
            if dscr >= 1.25:
                interpretations['dscr'] = 'Strong - Excellent debt coverage'
            elif dscr >= 1.0:
                interpretations['dscr'] = 'Adequate - Acceptable debt coverage'
            else:
                interpretations['dscr'] = 'Weak - Insufficient debt coverage'

        # 2. Debt to EBITDA interpretation
        debt_ebitda = ratios.get('debt_to_ebitda')
        if debt_ebitda is not None:
            if debt_ebitda <= 2.0:
                interpretations['debt_to_ebitda'] = 'Strong - Low leverage'
            elif debt_ebitda <= 4.0:
                interpretations['debt_to_ebitda'] = 'Moderate leverage'
            else:
                interpretations['debt_to_ebitda'] = 'High leverage - Risk concern'

        # 3. Current ratio interpretation
        current = ratios.get('current_ratio')
        if current is not None:
            if current >= 2.0:
                interpretations['current_ratio'] = 'Strong liquidity position'
            elif current >= 1.0:
                interpretations['current_ratio'] = 'Adequate liquidity'
            else:
                interpretations['current_ratio'] = 'Liquidity concerns'

        # 4. Quick ratio interpretation
        quick = ratios.get('quick_ratio')
        if quick is not None:
            if quick >= 1.0:
                interpretations['quick_ratio'] = 'Good immediate liquidity'
            elif quick >= 0.5:
                interpretations['quick_ratio'] = 'Acceptable liquidity'
            else:
                interpretations['quick_ratio'] = 'Weak immediate liquidity'

        # 5. Net Income Margin interpretation
        nim = ratios.get('net_income_margin')
        if nim is not None:
            if nim >= 10.0:
                interpretations['net_income_margin'] = 'Strong profitability'
            elif nim >= 5.0:
                interpretations['net_income_margin'] = 'Moderate profitability'
            else:
                interpretations['net_income_margin'] = 'Low profitability'

        # 6. Interest Coverage interpretation
        interest_cov = ratios.get('interest_coverage')
        if interest_cov is not None:
            if interest_cov >= 3.0:
                interpretations['interest_coverage'] = 'Strong - Excellent coverage'
            elif interest_cov >= 2.0:
                interpretations['interest_coverage'] = 'Adequate coverage'
            else:
                interpretations['interest_coverage'] = 'Weak - Risk concern'

        # 7. Leverage interpretation
        leverage = ratios.get('leverage_ratio')
        if leverage is not None:
            if leverage <= 0.3:
                interpretations['leverage_ratio'] = 'Low leverage - Conservative'
            elif leverage <= 0.6:
                interpretations['leverage_ratio'] = 'Moderate leverage - Balanced'
            else:
                interpretations['leverage_ratio'] = 'High leverage - Aggressive'

        # 8. Working Capital interpretation
        wc = ratios.get('working_capital')
        if wc is not None:
            if wc > 0:
                interpretations['working_capital'] = 'Positive - Good operational liquidity'
            else:
                interpretations['working_capital'] = 'Negative - Liquidity risk'

        # 9. DSO interpretation
        dso = ratios.get('dso')
        if dso is not None:
            if dso <= 45:
                interpretations['dso'] = 'Excellent - Fast collections'
            elif dso <= 60:
                interpretations['dso'] = 'Good collections'
            else:
                interpretations['dso'] = 'Slow collections - Risk concern'

        return interpretations


def test_calculator():
    """Test function to demonstrate calculations"""
    calc = FinancialCalculator()

    # Sample financial data with all required fields for 9 key ratios
    sample_data = {
        'revenue': 5000000,
        'net_income': 400000,
        'operating_income': 500000,
        'ebit': 550000,
        'ebitda': 600000,
        'debt_service': 350000,
        'total_debt': 2000000,
        'total_assets': 5000000,
        'total_equity': 3000000,
        'total_liabilities': 2000000,
        'current_assets': 1500000,
        'current_liabilities': 800000,
        'inventory': 300000,
        'accounts_receivable': 400000,
        'interest_expense': 100000,
        'cash_and_equivalents': 500000
    }

    print("Sample Financial Data:")
    for key, value in sample_data.items():
        print(f"  {key}: ${value:,.2f}")

    print("\n" + "="*60)
    print("CALCULATED RATIOS (9 Key Credit Analysis Ratios)")
    print("="*60)

    ratios = calc.calculate_all_ratios(sample_data)

    # Display 9 key ratios
    key_ratios = [
        ('dscr', 'Debt Service Coverage Ratio'),
        ('debt_to_ebitda', 'Total Debt to EBITDA'),
        ('current_ratio', 'Current Ratio'),
        ('quick_ratio', 'Quick Ratio'),
        ('net_income_margin', 'Net Income Margin'),
        ('interest_coverage', 'Interest Coverage Ratio'),
        ('leverage_ratio', 'Leverage Ratio'),
        ('working_capital', 'Working Capital'),
        ('dso', 'Days Sales Outstanding')
    ]

    for key, name in key_ratios:
        value = ratios.get(key)
        if value is not None:
            if key == 'working_capital':
                print(f"\n{name}: ${value:,.2f}")
            elif key in ['net_income_margin']:
                print(f"\n{name}: {value}%")
            elif key == 'dso':
                print(f"\n{name}: {value} days")
            else:
                print(f"\n{name}: {value}")

            # Print interpretation if available
            interp = ratios.get('interpretations', {}).get(key)
            if interp:
                print(f"  → {interp}")

    print("\n" + "="*60)


if __name__ == "__main__":
    test_calculator()
