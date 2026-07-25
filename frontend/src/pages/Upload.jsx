import React, { useState } from "react";
import { UploadCloud, File, X, CheckCircle } from "lucide-react";

function Upload({ setPage, setAnalysis }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
      setError("");
      setUploadProgress(0);
    } else {
      setError("Please select a valid PDF file");
      setFile(null);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.currentTarget.style.borderColor = "#ffffff";
    e.currentTarget.style.background = "rgba(255,255,255,0.15)";
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.currentTarget.style.borderColor = "rgba(255,255,255,0.3)";
    e.currentTarget.style.background = "rgba(255,255,255,0.05)";
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.currentTarget.style.borderColor = "rgba(255,255,255,0.3)";
    e.currentTarget.style.background = "rgba(255,255,255,0.05)";
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === "application/pdf") {
      setFile(droppedFile);
      setError("");
      setUploadProgress(0);
    } else {
      setError("Please select a valid PDF file");
      setFile(null);
    }
  };

  const removeFile = () => {
    setFile(null);
    setUploadProgress(0);
    setError("");
  };

  const analyze = async () => {
    if (!file) {
      setError("Please select a PDF file first");
      return;
    }

    setLoading(true);
    setError("");
    setUploadProgress(0);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 300);

      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        body: formData,
      });

      clearInterval(progressInterval);
      setUploadProgress(100);

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server error ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      setAnalysis(data);
      setPage("result");
    } catch (err) {
      console.error("Error:", err);
      setError(`Failed to analyze: ${err.message}`);
      setUploadProgress(0);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-page">
      {/* No mountains, no moon, no stars - Just gradient background */}
      
      {/* Upload Card */}
      <div className="upload-card">
        <h1>Upload Research Paper</h1>
        <p className="upload-subtitle">Upload your PDF to extract key information</p>

        {/* Drop Zone */}
        <div
          className={`drop-zone ${file ? "has-file" : ""}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          {!file ? (
            <>
              <UploadCloud className="upload-icon" size={48} />
              <p className="drop-text">Drag & drop your PDF here</p>
              <p className="drop-subtext">or click to browse</p>
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                className="file-input"
              />
            </>
          ) : (
            <div className="file-info">
              <File className="file-icon" size={32} />
              <div className="file-details">
                <span className="file-name">{file.name}</span>
                <span className="file-size">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </span>
              </div>
              <button className="remove-file" onClick={removeFile}>
                <X size={20} />
              </button>
            </div>
          )}
        </div>

        {/* Progress */}
        {uploadProgress > 0 && uploadProgress < 100 && (
          <div className="progress-container">
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
            <span className="progress-text">{uploadProgress}%</span>
          </div>
        )}

        {/* Success */}
        {uploadProgress === 100 && (
          <div className="success-message">
            <CheckCircle size={20} />
            <span>File uploaded successfully!</span>
          </div>
        )}

        {/* Error */}
        {error && <p className="upload-error">{error}</p>}

        {/* Analyze Button */}
        <button 
          className={`upload-btn ${loading ? "loading" : ""}`}
          onClick={analyze}
          disabled={!file || loading}
        >
          {loading ? (
            <>
              <span className="upload-spinner"></span>
              Analyzing...
            </>
          ) : (
            "Analyze Paper"
          )}
        </button>

        {/* Back Button */}
        <button 
          className="back-btn"
          onClick={() => setPage("login")}
        >
          ← Back to Login
        </button>
      </div>
    </div>
  );
}

export default Upload;