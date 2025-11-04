import React, { useState } from 'react';
import './App.css';
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
      <header className="App-header">
        <div className="header-content">
          <h1>Credit Memo Generator</h1>
          <p className="header-subtitle">
            Template-Adaptive AI Credit Memos • LandingAI ADE & AWS Bedrock
          </p>
          <p className="header-tagline">
            Eliminate manual copy-paste • Auto-extract data • Generate compliant memos
          </p>
        </div>
      </header>

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
        <p>
          Built for LandingAI Financial AI Hackathon Championship 2025
        </p>
        <p className="tech-stack">
          Tech Stack: LandingAI ADE API • AWS Bedrock • React • Flask
        </p>
      </footer>
    </div>
  );
}

export default App;
