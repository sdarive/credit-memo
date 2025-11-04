import React from 'react';
import './BankHeader.css';

function BankHeader() {
  return (
    <div className="bank-header">
      <div className="bank-header-content">
        <div className="bank-logo-section">
          <div className="bank-logo">
            <div className="logo-icon">
              <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                {/* Bank Building Icon */}
                <rect x="20" y="30" width="60" height="50" fill="#006747" />
                <rect x="25" y="35" width="8" height="10" fill="white" />
                <rect x="37" y="35" width="8" height="10" fill="white" />
                <rect x="49" y="35" width="8" height="10" fill="white" />
                <rect x="61" y="35" width="8" height="10" fill="white" />
                <rect x="25" y="50" width="8" height="10" fill="white" />
                <rect x="37" y="50" width="8" height="10" fill="white" />
                <rect x="49" y="50" width="8" height="10" fill="white" />
                <rect x="61" y="50" width="8" height="10" fill="white" />
                <rect x="15" y="75" width="70" height="5" fill="#006747" />
                <polygon points="50,15 85,30 15,30" fill="#006747" />
                <rect x="43" y="60" width="14" height="20" fill="white" />
              </svg>
            </div>
            <div className="bank-name">
              <h1>Midwest Regional Bank</h1>
              <p className="bank-tagline">Member FDIC</p>
            </div>
          </div>
        </div>
        <div className="app-title-section">
          <h2>Business & Commercial Finance</h2>
        </div>
      </div>
      <div className="bank-header-divider"></div>
    </div>
  );
}

export default BankHeader;
