import React, { useState } from 'react';
import './Upload.css';

function Upload({ onUploadComplete, onLoadingChange }) {
  const [file, setFile] = useState(null);
  const [borrowerName, setBorrowerName] = useState('');
  const [borrowerIndustry, setBorrowerIndustry] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    setLoading(true);
    setError(null);
    if (onLoadingChange) onLoadingChange(true);

    try {
      const formData = new FormData();
      formData.append('document', file);
      formData.append('borrower_name', borrowerName || 'Unknown Borrower');
      formData.append('borrower_industry', borrowerIndustry || 'Not specified');

      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Upload failed');
      }

      if (onUploadComplete) {
        onUploadComplete(data);
      }

      // Reset form
      setFile(null);
      setBorrowerName('');
      setBorrowerIndustry('');
      e.target.reset();

    } catch (err) {
      console.error('Upload error:', err);
      setError(err.message || 'Error uploading file. Please try again.');
    } finally {
      setLoading(false);
      if (onLoadingChange) onLoadingChange(false);
    }
  };

  const handleTestData = async () => {
    setLoading(true);
    setError(null);
    if (onLoadingChange) onLoadingChange(true);

    try {
      const response = await fetch('http://localhost:5000/test-extraction', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          borrower_name: borrowerName || 'Test Company Inc.',
          borrower_industry: borrowerIndustry || 'Manufacturing'
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Test failed');
      }

      if (onUploadComplete) {
        onUploadComplete(data);
      }

    } catch (err) {
      console.error('Test error:', err);
      setError(err.message || 'Error loading test data. Please try again.');
    } finally {
      setLoading(false);
      if (onLoadingChange) onLoadingChange(false);
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-card">
        <h2>Upload Financial Document</h2>
        <p className="subtitle">
          Upload borrower financial documents for automated credit memo generation
        </p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="borrower-name">Borrower Name (Optional)</label>
            <input
              type="text"
              id="borrower-name"
              placeholder="e.g., ABC Corporation"
              value={borrowerName}
              onChange={(e) => setBorrowerName(e.target.value)}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="borrower-industry">Industry (Optional)</label>
            <input
              type="text"
              id="borrower-industry"
              placeholder="e.g., Manufacturing, Retail, Services"
              value={borrowerIndustry}
              onChange={(e) => setBorrowerIndustry(e.target.value)}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="file-upload">Financial Document</label>
            <input
              type="file"
              id="file-upload"
              accept=".pdf,.doc,.docx,.xlsx,.xls,.csv"
              onChange={handleFileChange}
              disabled={loading}
            />
            <small className="hint">
              Accepted formats: PDF, Word, Excel, CSV (Max 16MB)
            </small>
          </div>

          {error && <div className="error-message">{error}</div>}

          {file && (
            <div className="file-info">
              Selected: <strong>{file.name}</strong> ({(file.size / 1024).toFixed(2)} KB)
            </div>
          )}

          <div className="button-group">
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading || !file}
            >
              {loading ? 'Processing...' : 'Upload & Analyze'}
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

        {loading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>Processing document with LandingAI and AWS Bedrock...</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Upload;
