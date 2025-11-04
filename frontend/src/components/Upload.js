import React, { useState, useRef } from 'react';
import './Upload.css';

function Upload({ onUploadComplete, onLoadingChange }) {
  const [files, setFiles] = useState([]);
  const [borrowerName, setBorrowerName] = useState('');
  const [borrowerIndustry, setBorrowerIndustry] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [processingStage, setProcessingStage] = useState('');
  const [progress, setProgress] = useState(0);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const newFiles = Array.from(e.dataTransfer.files);
      addFiles(newFiles);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const newFiles = Array.from(e.target.files);
      addFiles(newFiles);
    }
  };

  const addFiles = (newFiles) => {
    // LandingAI ADE only supports PDF, DOC, DOCX (not Excel/CSV)
    const validTypes = ['application/pdf', 'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];

    const validFiles = newFiles.filter(file => {
      const isValid = validTypes.includes(file.type) ||
        file.name.endsWith('.pdf') || file.name.endsWith('.doc') ||
        file.name.endsWith('.docx');

      if (!isValid) {
        setError(`${file.name} is not supported. Only PDF, DOC, and DOCX files are accepted (Excel/CSV not supported by LandingAI ADE).`);
      }
      return isValid;
    });

    setFiles(prevFiles => [...prevFiles, ...validFiles]);
    if (validFiles.length > 0) {
      setError(null);
    }
  };

  const removeFile = (index) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  const simulateProgress = () => {
    const stages = [
      { stage: 'Uploading documents...', progress: 10, delay: 500 },
      { stage: 'Extracting data with LandingAI ADE...', progress: 30, delay: 3000 },
      { stage: 'Analyzing financial metrics...', progress: 50, delay: 5000 },
      { stage: 'Calculating risk ratios...', progress: 70, delay: 2000 },
      { stage: 'Generating credit memo with AWS Bedrock...', progress: 85, delay: 8000 },
      { stage: 'Finalizing report...', progress: 95, delay: 1000 }
    ];

    let currentStage = 0;
    const updateStage = () => {
      if (currentStage < stages.length) {
        setProcessingStage(stages[currentStage].stage);
        setProgress(stages[currentStage].progress);
        currentStage++;
        setTimeout(updateStage, stages[currentStage - 1].delay);
      }
    };
    updateStage();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (files.length === 0) {
      setError('Please select at least one file to upload');
      return;
    }

    setLoading(true);
    setError(null);
    setProgress(0);
    setProcessingStage('Preparing upload...');
    if (onLoadingChange) onLoadingChange(true);

    // Start progress simulation
    simulateProgress();

    try {
      const formData = new FormData();

      // Add files with correct field name based on endpoint
      if (files.length === 1) {
        formData.append('document', files[0]);
      } else {
        files.forEach(file => {
          formData.append('documents', file);
        });
      }

      formData.append('borrower_name', borrowerName || 'Unknown Borrower');
      formData.append('borrower_industry', borrowerIndustry || 'Not specified');

      const endpoint = files.length === 1 ? 'upload' : 'upload-multiple';

      // Increase timeout for long-running analysis
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 180000); // 3 minute timeout

      const response = await fetch(`http://localhost:5001/${endpoint}`, {
        method: 'POST',
        body: formData,
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Upload failed');
      }

      setProgress(100);
      setProcessingStage('Complete!');

      // Normalize response format for multiple vs single file uploads
      let normalizedData = data;

      // If this is a multiple file upload response, extract the first successful result
      if (data.results && Array.isArray(data.results)) {
        const successfulResults = data.results.filter(r => r.success);
        const failedResults = data.results.filter(r => !r.success);

        if (successfulResults.length === 0) {
          // Check if error is API credits related
          const firstError = failedResults[0]?.error || '';
          if (firstError.includes('credits') || firstError.includes('Payment Required') || firstError.includes('insufficient')) {
            throw new Error(firstError);
          }
          const failedFiles = failedResults.map(r => r.filename).join(', ');
          throw new Error(`All documents failed to process: ${failedFiles}. ${firstError}`);
        }

        // For now, use the first successful result
        // TODO: In the future, we could aggregate all results or show a multi-document view
        normalizedData = successfulResults[0];

        // Add metadata about multiple files
        normalizedData.multiFileUpload = true;
        normalizedData.totalProcessed = data.processed;
        normalizedData.totalFailed = data.failed;
        normalizedData.processedFiles = successfulResults.map(r => r.filename);
        normalizedData.failedFiles = failedResults.map(r => ({ name: r.filename, error: r.error }));

        // Log info for user awareness
        console.log(`✓ Processed ${data.processed} documents successfully`);
        if (data.failed > 0) {
          console.warn(`⚠ ${data.failed} documents failed:`, normalizedData.failedFiles);
        }
      }

      if (onUploadComplete) {
        onUploadComplete(normalizedData);
      }

      // Reset form
      setTimeout(() => {
        setFiles([]);
        setBorrowerName('');
        setBorrowerIndustry('');
        if (fileInputRef.current) fileInputRef.current.value = '';
      }, 500);

    } catch (err) {
      console.error('Upload error:', err);
      if (err.name === 'AbortError') {
        setError('Request timed out. The analysis is taking longer than expected. Please try again or use test data.');
      } else {
        setError(err.message || 'Error uploading files. Please try again.');
      }
      setProgress(0);
      setProcessingStage('');
    } finally {
      setLoading(false);
      if (onLoadingChange) onLoadingChange(false);
    }
  };

  const handleTestData = async () => {
    console.log('🚀 Starting test data request...');
    setLoading(true);
    setError(null);
    setProgress(0);
    setProcessingStage('Loading test data...');
    if (onLoadingChange) onLoadingChange(true);

    // Realistic progress for test data (backend takes ~42 seconds total)
    const testStages = [
      { stage: 'Loading test data...', progress: 10, delay: 500 },
      { stage: 'Analyzing financial metrics...', progress: 25, delay: 2000 },
      { stage: 'Calculating risk ratios...', progress: 40, delay: 2000 },
      { stage: 'Generating AI credit memo with AWS Bedrock...', progress: 60, delay: 5000 },
      { stage: 'Finalizing credit memo (this takes 30-40 seconds)...', progress: 85, delay: 30000 }
    ];

    let currentStage = 0;
    const updateStage = () => {
      if (currentStage < testStages.length) {
        setProcessingStage(testStages[currentStage].stage);
        setProgress(testStages[currentStage].progress);
        currentStage++;
        setTimeout(updateStage, testStages[currentStage - 1].delay);
      }
    };
    updateStage();

    try {
      console.log('📡 Sending request to backend...');
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 180000); // 3 minute timeout for LLM generation

      const response = await fetch('http://localhost:5001/test-extraction', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          borrower_name: borrowerName || 'Test Company Inc.',
          borrower_industry: borrowerIndustry || 'Manufacturing'
        }),
        signal: controller.signal
      });

      console.log('📥 Response received. Status:', response.status, 'OK:', response.ok);
      clearTimeout(timeoutId);

      console.log('🔄 Parsing JSON response...');
      const data = await response.json();
      console.log('✅ JSON parsed successfully');
      console.log('📊 Response data keys:', Object.keys(data));
      console.log('📊 Has borrower_info:', !!data.borrower_info);
      console.log('📊 Has financial_data:', !!data.financial_data);
      console.log('📊 Has ratios:', !!data.ratios);
      console.log('📊 Has memo:', !!data.memo);

      if (!response.ok) {
        console.error('❌ Response not OK. Error:', data.error);
        throw new Error(data.error || 'Test failed');
      }

      setProgress(100);
      setProcessingStage('Complete!');

      console.log('🎉 Calling onUploadComplete callback...');
      if (onUploadComplete) {
        onUploadComplete(data);
        console.log('✅ Callback completed');
      } else {
        console.warn('⚠️ No onUploadComplete callback provided');
      }

    } catch (err) {
      console.error('❌ Test data error:', err);
      console.error('❌ Error name:', err.name);
      console.error('❌ Error message:', err.message);
      console.error('❌ Error stack:', err.stack);

      if (err.name === 'AbortError') {
        setError('Request timed out after 90 seconds. The AI memo generation is taking longer than expected. Please try again.');
      } else if (err.message && err.message.includes('Failed to fetch')) {
        setError('Network error: Cannot connect to backend at http://localhost:5001. Please ensure the backend is running.');
      } else if (err.name === 'SyntaxError') {
        setError('Invalid response from server. The backend returned malformed data.');
      } else {
        setError(err.message || 'Error loading test data. Please try again.');
      }
      setProgress(0);
      setProcessingStage('');
    } finally {
      console.log('🏁 Test data request completed (loading state cleared)');
      setLoading(false);
      if (onLoadingChange) onLoadingChange(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    else return (bytes / 1048576).toFixed(1) + ' MB';
  };

  return (
    <div className="upload-wrapper">
      <div className="upload-container">
        <div className="upload-header">
          <h1 className="upload-title">Credit Memo Generator</h1>
          <p className="upload-subtitle">
            AI-powered credit analysis using LandingAI ADE & AWS Bedrock
          </p>
        </div>

        <form onSubmit={handleSubmit} className="upload-form">
          {/* Borrower Information */}
          <div className="borrower-section">
            <h3 className="section-title">Borrower Information</h3>
            <div className="input-grid">
              <div className="input-group">
                <label htmlFor="borrower-name">Company Name</label>
                <input
                  type="text"
                  id="borrower-name"
                  placeholder="e.g., ABC Corporation"
                  value={borrowerName}
                  onChange={(e) => setBorrowerName(e.target.value)}
                  disabled={loading}
                  className="modern-input"
                />
              </div>

              <div className="input-group">
                <label htmlFor="borrower-industry">Industry</label>
                <input
                  type="text"
                  id="borrower-industry"
                  placeholder="e.g., Manufacturing, Retail"
                  value={borrowerIndustry}
                  onChange={(e) => setBorrowerIndustry(e.target.value)}
                  disabled={loading}
                  className="modern-input"
                />
              </div>
            </div>
          </div>

          {/* File Upload Area */}
          <div className="upload-section">
            <h3 className="section-title">Financial Documents</h3>

            <div
              className={`dropzone ${dragActive ? 'drag-active' : ''} ${files.length > 0 ? 'has-files' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                multiple
                accept=".pdf,.doc,.docx"
                onChange={handleFileChange}
                disabled={loading}
                className="file-input-hidden"
              />

              <div className="dropzone-content">
                <svg className="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <h4 className="dropzone-title">Drop files here or click to browse</h4>
                <p className="dropzone-hint">
                  Supports PDF and Word files only (up to 16MB each)
                </p>
                <p className="dropzone-hint" style={{ fontSize: '0.75rem', marginTop: '0.25rem', opacity: 0.8 }}>
                  Note: Excel/CSV not supported by LandingAI ADE
                </p>
              </div>
            </div>

            {/* File List */}
            {files.length > 0 && (
              <div className="file-list">
                <div className="file-list-header">
                  <span>{files.length} file{files.length !== 1 ? 's' : ''} selected</span>
                  <button
                    type="button"
                    onClick={() => setFiles([])}
                    className="clear-all-btn"
                    disabled={loading}
                  >
                    Clear all
                  </button>
                </div>
                {files.map((file, index) => (
                  <div key={index} className="file-item">
                    <div className="file-info">
                      <svg className="file-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      <div className="file-details">
                        <span className="file-name">{file.name}</span>
                        <span className="file-size">{formatFileSize(file.size)}</span>
                      </div>
                    </div>
                    <button
                      type="button"
                      onClick={() => removeFile(index)}
                      className="remove-file-btn"
                      disabled={loading}
                      aria-label="Remove file"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {error && (
            <div className="error-banner">
              <svg className="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{error}</span>
            </div>
          )}

          {/* Progress Indicator */}
          {loading && processingStage && (
            <div className="progress-section">
              <div className="progress-header">
                <div className="progress-icon-wrapper">
                  <svg className="progress-icon spinning" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </div>
                <div className="progress-text">
                  <h4 className="progress-stage">{processingStage}</h4>
                  <p className="progress-hint">This may take 30-60 seconds for document analysis</p>
                </div>
              </div>
              <div className="progress-bar-container">
                <div className="progress-bar" style={{ width: `${progress}%` }}>
                  <div className="progress-bar-shine"></div>
                </div>
                <span className="progress-percentage">{progress}%</span>
              </div>
              <div className="progress-stages">
                <div className={`stage-item ${progress >= 10 ? 'completed' : ''} ${progress < 10 && progress > 0 ? 'active' : ''}`}>
                  <div className="stage-dot"></div>
                  <span className="stage-label">Upload</span>
                </div>
                <div className={`stage-item ${progress >= 30 ? 'completed' : ''} ${progress < 30 && progress >= 10 ? 'active' : ''}`}>
                  <div className="stage-dot"></div>
                  <span className="stage-label">Extract</span>
                </div>
                <div className={`stage-item ${progress >= 70 ? 'completed' : ''} ${progress < 70 && progress >= 30 ? 'active' : ''}`}>
                  <div className="stage-dot"></div>
                  <span className="stage-label">Analyze</span>
                </div>
                <div className={`stage-item ${progress >= 85 ? 'completed' : ''} ${progress < 85 && progress >= 70 ? 'active' : ''}`}>
                  <div className="stage-dot"></div>
                  <span className="stage-label">Generate</span>
                </div>
                <div className={`stage-item ${progress === 100 ? 'completed' : ''} ${progress < 100 && progress >= 85 ? 'active' : ''}`}>
                  <div className="stage-dot"></div>
                  <span className="stage-label">Complete</span>
                </div>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="action-buttons">
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading || files.length === 0}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Processing...
                </>
              ) : (
                <>
                  <svg className="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Analyze Document{files.length > 1 ? 's' : ''}
                </>
              )}
            </button>

            <button
              type="button"
              className="btn btn-secondary"
              onClick={handleTestData}
              disabled={loading}
            >
              {loading ? 'Loading...' : 'Use Test Data'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Upload;
