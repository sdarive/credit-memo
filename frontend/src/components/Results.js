import React from 'react';
import './Results.css';

function Results({ data }) {
  if (!data) {
    return null;
  }

  const { borrower_info, financial_data, ratios } = data;

  const formatCurrency = (value) => {
    if (value === null || value === undefined) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatRatio = (value) => {
    if (value === null || value === undefined) return 'N/A';
    return value.toFixed(2);
  };

  const getRatioClass = (ratioName, value) => {
    if (value === null || value === undefined) return '';

    switch (ratioName) {
      case 'dscr':
        return value >= 1.25 ? 'good' : value >= 1.0 ? 'fair' : 'poor';
      case 'leverage_ratio':
        return value <= 0.3 ? 'good' : value <= 0.6 ? 'fair' : 'poor';
      case 'current_ratio':
      case 'quick_ratio':
        return value >= 2.0 ? 'good' : value >= 1.0 ? 'fair' : 'poor';
      default:
        return '';
    }
  };

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>Analysis Results</h2>
        {borrower_info && (
          <div className="borrower-info">
            <div className="info-item">
              <span className="label">Borrower:</span>
              <span className="value">{borrower_info.name}</span>
            </div>
            <div className="info-item">
              <span className="label">Industry:</span>
              <span className="value">{borrower_info.industry}</span>
            </div>
          </div>
        )}
      </div>

      <div className="results-grid">
        {/* Financial Data Section */}
        <div className="results-section">
          <h3>Financial Data</h3>
          <div className="data-grid">
            <div className="data-item">
              <span className="data-label">Revenue</span>
              <span className="data-value">{formatCurrency(financial_data.revenue)}</span>
            </div>
            <div className="data-item">
              <span className="data-label">Net Income</span>
              <span className="data-value">{formatCurrency(financial_data.net_income)}</span>
            </div>
            <div className="data-item">
              <span className="data-label">Total Assets</span>
              <span className="data-value">{formatCurrency(financial_data.total_assets)}</span>
            </div>
            <div className="data-item">
              <span className="data-label">Total Liabilities</span>
              <span className="data-value">{formatCurrency(financial_data.total_liabilities)}</span>
            </div>
            <div className="data-item">
              <span className="data-label">Total Debt</span>
              <span className="data-value">{formatCurrency(financial_data.total_debt)}</span>
            </div>
            <div className="data-item">
              <span className="data-label">Total Equity</span>
              <span className="data-value">{formatCurrency(financial_data.total_equity)}</span>
            </div>
            <div className="data-item">
              <span className="data-label">Cash & Equivalents</span>
              <span className="data-value">{formatCurrency(financial_data.cash_and_equivalents)}</span>
            </div>
            <div className="data-item">
              <span className="data-label">Operating Income</span>
              <span className="data-value">{formatCurrency(financial_data.operating_income)}</span>
            </div>
          </div>
        </div>

        {/* Financial Ratios Section */}
        <div className="results-section">
          <h3>Key Financial Ratios</h3>
          <div className="ratios-grid">
            <div className={`ratio-card ${getRatioClass('dscr', ratios.dscr)}`}>
              <div className="ratio-name">DSCR</div>
              <div className="ratio-value">{formatRatio(ratios.dscr)}</div>
              {ratios.interpretations?.dscr && (
                <div className="ratio-interpretation">{ratios.interpretations.dscr}</div>
              )}
            </div>

            <div className={`ratio-card ${getRatioClass('leverage_ratio', ratios.leverage_ratio)}`}>
              <div className="ratio-name">Leverage Ratio</div>
              <div className="ratio-value">{formatRatio(ratios.leverage_ratio)}</div>
              {ratios.interpretations?.leverage && (
                <div className="ratio-interpretation">{ratios.interpretations.leverage}</div>
              )}
            </div>

            <div className={`ratio-card ${getRatioClass('current_ratio', ratios.current_ratio)}`}>
              <div className="ratio-name">Current Ratio</div>
              <div className="ratio-value">{formatRatio(ratios.current_ratio)}</div>
              {ratios.interpretations?.current_ratio && (
                <div className="ratio-interpretation">{ratios.interpretations.current_ratio}</div>
              )}
            </div>

            <div className={`ratio-card ${getRatioClass('quick_ratio', ratios.quick_ratio)}`}>
              <div className="ratio-name">Quick Ratio</div>
              <div className="ratio-value">{formatRatio(ratios.quick_ratio)}</div>
            </div>

            <div className="ratio-card">
              <div className="ratio-name">Debt-to-Equity</div>
              <div className="ratio-value">{formatRatio(ratios.debt_to_equity)}</div>
            </div>

            <div className="ratio-card">
              <div className="ratio-name">ROA</div>
              <div className="ratio-value">{formatRatio(ratios.roa)}%</div>
            </div>

            <div className="ratio-card">
              <div className="ratio-name">ROE</div>
              <div className="ratio-value">{formatRatio(ratios.roe)}%</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Results;
