import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './MemoEditor.css';

function MemoEditor({ memo, borrowerInfo, financialData, ratios }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedMemo, setEditedMemo] = useState(memo);
  const [isGeneratingWord, setIsGeneratingWord] = useState(false);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = () => {
    setIsEditing(false);
    // Could add API call here to save edited memo
  };

  const handleCancel = () => {
    setEditedMemo(memo);
    setIsEditing(false);
  };

  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([editedMemo], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    const borrowerName = borrowerInfo?.name || 'Borrower';
    const filename = `Credit_Memo_${borrowerName.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.txt`;
    element.download = filename;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(editedMemo);
    alert('Memo copied to clipboard!');
  };

  const handleDownloadWord = async () => {
    setIsGeneratingWord(true);

    try {
      const response = await fetch('http://localhost:5001/download-word', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          financial_data: financialData,
          ratios: ratios,
          memo: editedMemo,
          borrower_info: borrowerInfo
        })
      });

      if (!response.ok) {
        throw new Error('Failed to generate Word document');
      }

      // Download file
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const borrowerName = borrowerInfo?.name || 'Borrower';
      a.download = `Credit_Memo_${borrowerName.replace(/\s+/g, '_')}.docx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      alert('Word document downloaded successfully!');
    } catch (error) {
      console.error('Error downloading Word document:', error);
      alert('Failed to generate Word document. Please try again.');
    } finally {
      setIsGeneratingWord(false);
    }
  };

  if (!memo) {
    return null;
  }

  return (
    <div className="memo-editor-container">
      <div className="memo-editor-card">
        <div className="memo-header">
          <h2>Credit Memo</h2>
          <div className="memo-actions">
            {!isEditing ? (
              <>
                <button className="btn btn-edit" onClick={handleEdit}>
                  Edit
                </button>
                <button className="btn btn-copy" onClick={handleCopy}>
                  Copy
                </button>
                <button className="btn btn-download" onClick={handleDownload}>
                  Download TXT
                </button>
                <button
                  className="btn btn-download-word"
                  onClick={handleDownloadWord}
                  disabled={isGeneratingWord}
                >
                  {isGeneratingWord ? '📄 Generating...' : '📄 Download Word'}
                </button>
              </>
            ) : (
              <>
                <button className="btn btn-save" onClick={handleSave}>
                  Save
                </button>
                <button className="btn btn-cancel" onClick={handleCancel}>
                  Cancel
                </button>
              </>
            )}
          </div>
        </div>

        <div className="memo-content">
          {isEditing ? (
            <textarea
              className="memo-textarea"
              value={editedMemo}
              onChange={(e) => setEditedMemo(e.target.value)}
              autoFocus
            />
          ) : (
            <div className="memo-display">
              <ReactMarkdown>{editedMemo}</ReactMarkdown>
            </div>
          )}
        </div>

        <div className="memo-footer">
          <small className="memo-disclaimer">
            This credit memo was generated using AI-powered analysis. Please review and verify all information before use in lending decisions.
          </small>
        </div>
      </div>
    </div>
  );
}

export default MemoEditor;
