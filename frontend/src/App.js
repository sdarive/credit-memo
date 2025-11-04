import React, { useState } from 'react';
import './App.css';
import BankHeader from './components/BankHeader';
import Upload from './components/Upload';
import Results from './components/Results';
import MemoEditor from './components/MemoEditor';

function App() {
  const [analysisData, setAnalysisData] = useState(null);

  const handleUploadComplete = (data) => {
    console.log('📋 App.js: handleUploadComplete called');
    console.log('📋 App.js: Received data:', data);
    console.log('📋 App.js: Data type:', typeof data);
    console.log('📋 App.js: Data keys:', data ? Object.keys(data) : 'null');

    try {
      setAnalysisData(data);
      console.log('✅ App.js: Analysis data set successfully');
    } catch (err) {
      console.error('❌ App.js: Error setting analysis data:', err);
    }
  };

  const handleLoadingChange = (loading) => {
    // Loading state is now handled by Upload component
  };

  const handleReset = () => {
    setAnalysisData(null);
  };

  return (
    <div className="App">
      <BankHeader />

      <main className="App-main">
        {!analysisData && (
          <Upload
            onUploadComplete={handleUploadComplete}
            onLoadingChange={handleLoadingChange}
          />
        )}

        {analysisData && (
          <>
            <div className="action-bar">
              <button className="btn btn-reset" onClick={handleReset}>
                ← New Analysis
              </button>
            </div>

            <Results data={analysisData} />

            {analysisData.memo && (
              <MemoEditor
                memo={analysisData.memo}
                borrowerInfo={analysisData.borrower_info}
                financialData={analysisData.financial_data}
                ratios={analysisData.ratios}
              />
            )}
          </>
        )}
      </main>

      <footer className="App-footer">
        <div className="footer-content">
          <div className="footer-section">
            <p className="footer-disclaimer">
              © 2025 Midwest Regional Bank. Ernie - Your Assistant for Credit Memos.
            </p>
            <p className="footer-note">
              This AI-powered platform is designed to assist credit analysts. All credit decisions require human review and approval.
            </p>
          </div>
          <div className="footer-tech">
            <p className="tech-label">AI credit processing technology</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
