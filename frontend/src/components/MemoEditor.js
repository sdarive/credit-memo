import React, { useState } from 'react';
import './MemoEditor.css';

function MemoEditor({ memo, borrowerInfo }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedMemo, setEditedMemo] = useState(memo);

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
                  Download
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
            <pre className="memo-display">{editedMemo}</pre>
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
