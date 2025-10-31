import React, { useState } from 'react';
import './App.css';
import Upload from './components/Upload';
import Results from './components/Results';
import MemoEditor from './components/MemoEditor';

function App() {
  const [analysisData, setAnalysisData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleUploadComplete = (data) => {
    console.log('Analysis complete:', data);
    setAnalysisData(data);
  };

  const handleLoadingChange = (loading) => {
    setIsLoading(loading);
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
            Automated credit analysis powered by LandingAI ADE & AWS Bedrock
          </p>
        </div>
      </header>

      <main className="App-main">
        {!analysisData && !isLoading && (
          <Upload
            onUploadComplete={handleUploadComplete}
            onLoadingChange={handleLoadingChange}
          />
        )}

        {isLoading && (
          <div className="loading-screen">
            <div className="loading-spinner"></div>
            <h2>Analyzing Document...</h2>
            <p>Extracting financial data with LandingAI ADE</p>
            <p>Calculating credit ratios</p>
            <p>Generating memo with AWS Bedrock</p>
          </div>
        )}

        {analysisData && !isLoading && (
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
