import React from "react";

function Result({ analysis, setPage }) {
  if (!analysis) {
    return (
      <div 
        className="result-container-dark" 
        style={{ 
          overflowY: "auto", 
          height: "100vh",
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          zIndex: 9999,
          padding: "40px 20px 80px 20px",
          background: "linear-gradient(135deg, #1a0a2e 0%, #2d1b4e 50%, #1a0a2e 100%)",
          display: "flex",
          justifyContent: "center"
        }}
      >
        <div className="result-content-dark" style={{ maxWidth: "1000px", width: "100%" }}>
          <div className="premium-card-dark" style={{ 
            textAlign: "center",
            background: "rgba(255,255,255,0.06)",
            borderRadius: "16px",
            padding: "30px",
            boxShadow: "0 4px 30px rgba(0,0,0,0.4)",
            border: "1px solid rgba(255,255,255,0.06)",
            backdropFilter: "blur(10px)"
          }}>
            <h2 style={{ color: "#ffffff" }}>No analysis data available</h2>
            <p style={{ color: "#94a3b8" }}>Please upload a paper first.</p>
            <button 
              className="premium-btn-dark center-btn" 
              onClick={() => setPage("upload")}
              style={{
                background: "linear-gradient(135deg, #7c3aed, #6d28d9)",
                color: "white",
                border: "none",
                padding: "14px 35px",
                borderRadius: "12px",
                fontSize: "16px",
                fontWeight: "600",
                cursor: "pointer",
                transition: "all 0.3s ease",
                boxShadow: "0 4px 20px rgba(124,58,237,0.25)",
                marginTop: "20px"
              }}
            >
              Go to Upload
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (analysis.error) {
    return (
      <div 
        className="result-container-dark" 
        style={{ 
          overflowY: "auto", 
          height: "100vh",
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          zIndex: 9999,
          padding: "40px 20px 80px 20px",
          background: "linear-gradient(135deg, #1a0a2e 0%, #2d1b4e 50%, #1a0a2e 100%)",
          display: "flex",
          justifyContent: "center"
        }}
      >
        <div className="result-content-dark" style={{ maxWidth: "1000px", width: "100%" }}>
          <div className="premium-card-dark" style={{ 
            textAlign: "center",
            background: "rgba(255,255,255,0.06)",
            borderRadius: "16px",
            padding: "30px",
            boxShadow: "0 4px 30px rgba(0,0,0,0.4)",
            border: "1px solid rgba(255,255,255,0.06)",
            backdropFilter: "blur(10px)"
          }}>
            <h2 style={{ color: "#ffffff" }}>❌ Error</h2>
            <p style={{ color: "#94a3b8" }}>{analysis.error}</p>
            <button 
              className="premium-btn-dark center-btn" 
              onClick={() => setPage("upload")}
              style={{
                background: "linear-gradient(135deg, #7c3aed, #6d28d9)",
                color: "white",
                border: "none",
                padding: "14px 35px",
                borderRadius: "12px",
                fontSize: "16px",
                fontWeight: "600",
                cursor: "pointer",
                transition: "all 0.3s ease",
                boxShadow: "0 4px 20px rgba(124,58,237,0.25)",
                marginTop: "20px"
              }}
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  const renderValue = (value) => {
    if (!value || value === "N/A" || value === "Not found" || 
        value === "Title not found" || value === "Authors not found" ||
        value === "Year not found" || value === "Abstract not found" ||
        value === "Methodology not clearly described" ||
        value === "Dataset information not specified" ||
        value === "Results not clearly presented" ||
        value === "Future scope not specified" ||
        value === "Advantages not clearly stated") {
      return <p style={{ color: "#94a3b8", fontStyle: "italic" }}>Not available</p>;
    }
    
    if (Array.isArray(value)) {
      if (value.length === 0) {
        return <p style={{ color: "#94a3b8", fontStyle: "italic" }}>Not available</p>;
      }
      return (
        <ul style={{ paddingLeft: "20px", margin: "5px 0" }}>
          {value.map((item, idx) => (
            <li key={idx} style={{
              color: "#e2e8f0",
              fontSize: "15px",
              lineHeight: "1.7",
              margin: "5px 0",
              listStyleType: "none",
              position: "relative",
              paddingLeft: "20px"
            }}>
              {item}
            </li>
          ))}
        </ul>
      );
    }
    
    if (typeof value === "string" && value.includes(" | ")) {
      const items = value.split(" | ").map(item => item.trim()).filter(item => item.length > 0);
      if (items.length > 1) {
        return (
          <ul style={{ paddingLeft: "20px", margin: "5px 0" }}>
            {items.map((item, idx) => (
              <li key={idx} style={{
                color: "#e2e8f0",
                fontSize: "15px",
                lineHeight: "1.7",
                margin: "5px 0",
                listStyleType: "none",
                position: "relative",
                paddingLeft: "20px"
              }}>
                {item}
              </li>
            ))}
          </ul>
        );
      }
    }
    
    if (typeof value === "string" && value.includes("; ")) {
      const items = value.split("; ").map(item => item.trim()).filter(item => item.length > 0);
      if (items.length > 1) {
        return (
          <ul style={{ paddingLeft: "20px", margin: "5px 0" }}>
            {items.map((item, idx) => (
              <li key={idx} style={{
                color: "#e2e8f0",
                fontSize: "15px",
                lineHeight: "1.7",
                margin: "5px 0",
                listStyleType: "none",
                position: "relative",
                paddingLeft: "20px"
              }}>
                {item}
              </li>
            ))}
          </ul>
        );
      }
    }
    
    if (typeof value === "string") {
      return <p style={{ color: "#e2e8f0", fontSize: "15px", lineHeight: "1.7" }}>{value}</p>;
    }
    
    return <p style={{ color: "#e2e8f0", fontSize: "15px", lineHeight: "1.7" }}>{String(value)}</p>;
  };

  const renderAlgorithms = (value) => {
    if (!value || value === "Not specified" || value === "N/A") {
      return <p style={{ color: "#94a3b8", fontStyle: "italic" }}>Not specified</p>;
    }
    
    if (Array.isArray(value)) {
      return renderValue(value);
    }
    
    if (typeof value === "string") {
      if (value.includes(" | ")) {
        const items = value.split(" | ").map(item => item.trim()).filter(item => item.length > 0);
        if (items.length > 1) {
          return (
            <ul style={{ paddingLeft: "20px", margin: "5px 0" }}>
              {items.map((item, idx) => (
                <li key={idx} style={{
                  color: "#e2e8f0",
                  fontSize: "15px",
                  lineHeight: "1.7",
                  margin: "5px 0",
                  listStyleType: "none",
                  position: "relative",
                  paddingLeft: "20px"
                }}>
                  {item}
                </li>
              ))}
            </ul>
          );
        }
      }
      
      if (value.includes("; ")) {
        const items = value.split("; ").map(item => item.trim()).filter(item => item.length > 0);
        if (items.length > 1) {
          return (
            <ul style={{ paddingLeft: "20px", margin: "5px 0" }}>
              {items.map((item, idx) => (
                <li key={idx} style={{
                  color: "#e2e8f0",
                  fontSize: "15px",
                  lineHeight: "1.7",
                  margin: "5px 0",
                  listStyleType: "none",
                  position: "relative",
                  paddingLeft: "20px"
                }}>
                  {item}
                </li>
              ))}
            </ul>
          );
        }
      }
      
      if (value.includes(", ")) {
        const items = value.split(", ").map(item => item.trim()).filter(item => item.length > 0);
        if (items.length > 1) {
          return (
            <ul style={{ paddingLeft: "20px", margin: "5px 0" }}>
              {items.map((item, idx) => (
                <li key={idx} style={{
                  color: "#e2e8f0",
                  fontSize: "15px",
                  lineHeight: "1.7",
                  margin: "5px 0",
                  listStyleType: "none",
                  position: "relative",
                  paddingLeft: "20px"
                }}>
                  {item}
                </li>
              ))}
            </ul>
          );
        }
      }
      
      return <p style={{ color: "#e2e8f0", fontSize: "15px", lineHeight: "1.7" }}>{value}</p>;
    }
    
    return <p style={{ color: "#e2e8f0", fontSize: "15px", lineHeight: "1.7" }}>{String(value)}</p>;
  };

  const renderAdvantages = (value) => {
    if (!value || value === "Advantages not clearly stated" || value === "N/A") {
      return <p style={{ color: "#94a3b8", fontStyle: "italic" }}>Not available</p>;
    }
    
    if (Array.isArray(value)) {
      return renderValue(value);
    }
    
    if (typeof value === "string") {
      if (value.includes(" | ")) {
        const items = value.split(" | ").map(item => item.trim()).filter(item => item.length > 0);
        if (items.length > 1) {
          return (
            <ul style={{ paddingLeft: "20px", margin: "5px 0" }}>
              {items.map((item, idx) => (
                <li key={idx} style={{
                  color: "#e2e8f0",
                  fontSize: "15px",
                  lineHeight: "1.7",
                  margin: "5px 0",
                  listStyleType: "none",
                  position: "relative",
                  paddingLeft: "20px"
                }}>
                  {item}
                </li>
              ))}
            </ul>
          );
        }
      }
      
      if (value.includes("; ")) {
        const items = value.split("; ").map(item => item.trim()).filter(item => item.length > 0);
        if (items.length > 1) {
          return (
            <ul style={{ paddingLeft: "20px", margin: "5px 0" }}>
              {items.map((item, idx) => (
                <li key={idx} style={{
                  color: "#e2e8f0",
                  fontSize: "15px",
                  lineHeight: "1.7",
                  margin: "5px 0",
                  listStyleType: "none",
                  position: "relative",
                  paddingLeft: "20px"
                }}>
                  {item}
                </li>
              ))}
            </ul>
          );
        }
      }
      
      return <p style={{ color: "#e2e8f0", fontSize: "15px", lineHeight: "1.7" }}>{value}</p>;
    }
    
    return <p style={{ color: "#e2e8f0", fontSize: "15px", lineHeight: "1.7" }}>{String(value)}</p>;
  };

  return (
    <div 
      className="result-container-dark" 
      style={{ 
        overflowY: "auto", 
        height: "100vh",
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        zIndex: 9999,
        padding: "40px 20px 80px 20px",
        background: "linear-gradient(135deg, #1a0a2e 0%, #2d1b4e 50%, #1a0a2e 100%)",
        display: "flex",
        justifyContent: "center",
        scrollBehavior: "smooth"
      }}
    >
      <div className="result-content-dark" style={{ maxWidth: "1000px", width: "100%" }}>
        <h1 className="result-title-dark" style={{
          textAlign: "center",
          color: "#ffffff",
          fontSize: "36px",
          fontWeight: "700",
          marginBottom: "5px",
          letterSpacing: "1px",
          textShadow: "0 0 30px rgba(124,58,237,0.15)"
        }}>
          📄 Research Paper Analysis Report
        </h1>

        {analysis.processing_time && (
          <div className="processing-time-dark" style={{
            textAlign: "center",
            color: "#8888bb",
            fontSize: "14px",
            marginBottom: "30px"
          }}>
            ⏱️ Processing time: {analysis.processing_time}
          </div>
        )}

        <div className="result-grid-dark" style={{
          display: "flex",
          flexDirection: "column",
          gap: "20px",
          marginBottom: "30px",
          width: "100%"
        }}>
          {/* Title */}
          <div className="premium-card-dark full-width" style={{
            background: "rgba(255,255,255,0.06)",
            borderRadius: "16px",
            padding: "22px 25px",
            boxShadow: "0 4px 30px rgba(0,0,0,0.4)",
            border: "1px solid rgba(255,255,255,0.06)",
            transition: "all 0.3s ease",
            backdropFilter: "blur(10px)",
            width: "100%",
            boxSizing: "border-box"
          }}>
            <h2 style={{
              color: "#a78bfa",
              fontSize: "18px",
              fontWeight: "600",
              marginBottom: "10px",
              display: "flex",
              alignItems: "center",
              gap: "10px"
            }}>
              <span className="icon" style={{ fontSize: "20px" }}>📌</span> Title
            </h2>
            {renderValue(analysis.title)}
          </div>

          {/* Publication Year */}
          <div className="premium-card-dark" style={{
            background: "rgba(255,255,255,0.06)",
            borderRadius: "16px",
            padding: "22px 25px",
            boxShadow: "0 4px 30px rgba(0,0,0,0.4)",
            border: "1px solid rgba(255,255,255,0.06)",
            transition: "all 0.3s ease",
            backdropFilter: "blur(10px)",
            width: "100%",
            boxSizing: "border-box"
          }}>
            <h2 style={{
              color: "#a78bfa",
              fontSize: "18px",
              fontWeight: "600",
              marginBottom: "10px",
              display: "flex",
              alignItems: "center",
              gap: "10px"
            }}>
              <span className="icon" style={{ fontSize: "20px" }}>📅</span> Publication Year
            </h2>
            {renderValue(analysis.publication_year)}
          </div>

          {/* Research Domain */}
          <div className="premium-card-dark" style={{
            background: "rgba(255,255,255,0.06)",
            borderRadius: "16px",
            padding: "22px 25px",
            boxShadow: "0 4px 30px rgba(0,0,0,0.4)",
            border: "1px solid rgba(255,255,255,0.06)",
            transition: "all 0.3s ease",
            backdropFilter: "blur(10px)",
            width: "100%",
            boxSizing: "border-box"
          }}>
            <h2 style={{
              color: "#a78bfa",
              fontSize: "18px",
              fontWeight: "600",
              marginBottom: "10px",
              display: "flex",
              alignItems: "center",
              gap: "10px"
            }}>
              <span className="icon" style={{ fontSize: "20px" }}>🔬</span> Research Domain
            </h2>
            {renderValue(analysis.research_domain)}
          </div>

          {/* Abstract Summary */}
          <div className="premium-card-dark full-width" style={{
            background: "rgba(255,255,255,0.06)",
            borderRadius: "16px",
            padding: "22px 25px",
            boxShadow: "0 4px 30px rgba(0,0,0,0.4)",
            border: "1px solid rgba(255,255,255,0.06)",
            transition: "all 0.3s ease",
            backdropFilter: "blur(10px)",
            width: "100%",
            boxSizing: "border-box"
          }}>
            <h2 style={{
              color: "#a78bfa",
              fontSize: "18px",
              fontWeight: "600",
              marginBottom: "10px",
              display: "flex",
              alignItems: "center",
              gap: "10px"
            }}>
              <span className="icon" style={{ fontSize: "20px" }}>📝</span> Abstract Summary
            </h2>
            {renderValue(analysis.abstract_summary)}
          </div>

          {/* Keywords */}
          <div className="premium-card-dark full-width" style={{
            background: "rgba(255,255,255,0.06)",
            borderRadius: "16px",
            padding: "22px 25px",
            boxShadow: "0 4px 30px rgba(0,0,0,0.4)",
            border: "1px solid rgba(255,255,255,0.06)",
            transition: "all 0.3s ease",
            backdropFilter: "blur(10px)",
            width: "100%",
            boxSizing: "border-box"
          }}>
            <h2 style={{
              color: "#a78bfa",
              fontSize: "18px",
              fontWeight: "600",
              marginBottom: "10px",
              display: "flex",
              alignItems: "center",
              gap: "10px"
            }}>
              <span className="icon" style={{ fontSize: "20px" }}>🔑</span> Keywords
            </h2>
            {renderValue(analysis.keywords)}
          </div>

          {/* Methodology */}
          <div className="premium-card-dark full-width" style={{
            background: "rgba(255,255,255,0.06)",
            borderRadius: "16px",
            padding: "22px 25px",
            boxShadow: "0 4px 30px rgba(0,0,0,0.4)",
            border: "1px solid rgba(255,255,255,0.06)",
            transition: "all 0.3s ease",
            backdropFilter: "blur(10px)",
            width: "100%",
            boxSizing: "border-box"
          }}>
            <h2 style={{
              color: "#a78bfa",
              fontSize: "18px",
              fontWeight: "600",
              marginBottom: "10px",
              display: "flex",
              alignItems: "center",
              gap: "10px"
            }}>
              <span className="icon" style={{ fontSize: "20px" }}>⚙️</span> Methodology
            </h2>
            {renderValue(analysis.methodology)}
          </div>

          {/* Algorithms Used */}
          <div className="premium-card-dark full-width" style={{
            background: "rgba(255,255,255,0.06)",
            borderRadius: "16px",
            padding: "22px 25px",
            boxShadow: "0 4px 30px rgba(0,0,0,0.4)",
            border: "1px solid rgba(255,255,255,0.06)",
            transition: "all 0.3s ease",
            backdropFilter: "blur(10px)",
            width: "100%",
            boxSizing: "border-box"
          }}>
            <h2 style={{
              color: "#a78bfa",
              fontSize: "18px",
              fontWeight: "600",
              marginBottom: "10px",
              display: "flex",
              alignItems: "center",
              gap: "10px"
            }}>
              <span className="icon" style={{ fontSize: "20px" }}>🤖</span> Algorithms Used
            </h2>
            {renderAlgorithms(analysis.algorithms_used)}
          </div>

          {/* Dataset Information */}
          <div className="premium-card-dark full-width" style={{
            background: "rgba(255,255,255,0.06)",
            borderRadius: "16px",
            padding: "22px 25px",
            boxShadow: "0 4px 30px rgba(0,0,0,0.4)",
            border: "1px solid rgba(255,255,255,0.06)",
            transition: "all 0.3s ease",
            backdropFilter: "blur(10px)",
            width: "100%",
            boxSizing: "border-box"
          }}>
            <h2 style={{
              color: "#a78bfa",
              fontSize: "18px",
              fontWeight: "600",
              marginBottom: "10px",
              display: "flex",
              alignItems: "center",
              gap: "10px"
            }}>
              <span className="icon" style={{ fontSize: "20px" }}>📊</span> Dataset Information
            </h2>
            {renderValue(analysis.dataset_information)}
          </div>

          {/* Results */}
          <div className="premium-card-dark full-width" style={{
            background: "rgba(255,255,255,0.06)",
            borderRadius: "16px",
            padding: "22px 25px",
            boxShadow: "0 4px 30px rgba(0,0,0,0.4)",
            border: "1px solid rgba(255,255,255,0.06)",
            transition: "all 0.3s ease",
            backdropFilter: "blur(10px)",
            width: "100%",
            boxSizing: "border-box"
          }}>
            <h2 style={{
              color: "#a78bfa",
              fontSize: "18px",
              fontWeight: "600",
              marginBottom: "10px",
              display: "flex",
              alignItems: "center",
              gap: "10px"
            }}>
              <span className="icon" style={{ fontSize: "20px" }}>📈</span> Results
            </h2>
            {renderValue(analysis.results)}
          </div>

          {/* Advantages */}
          <div className="premium-card-dark full-width" style={{
            background: "rgba(255,255,255,0.06)",
            borderRadius: "16px",
            padding: "22px 25px",
            boxShadow: "0 4px 30px rgba(0,0,0,0.4)",
            border: "1px solid rgba(255,255,255,0.06)",
            transition: "all 0.3s ease",
            backdropFilter: "blur(10px)",
            width: "100%",
            boxSizing: "border-box"
          }}>
            <h2 style={{
              color: "#a78bfa",
              fontSize: "18px",
              fontWeight: "600",
              marginBottom: "10px",
              display: "flex",
              alignItems: "center",
              gap: "10px"
            }}>
              <span className="icon" style={{ fontSize: "20px" }}>✅</span> Advantages
            </h2>
            {renderAdvantages(analysis.advantages)}
          </div>

          {/* Future Scope */}
          <div className="premium-card-dark full-width" style={{
            background: "rgba(255,255,255,0.06)",
            borderRadius: "16px",
            padding: "22px 25px",
            boxShadow: "0 4px 30px rgba(0,0,0,0.4)",
            border: "1px solid rgba(255,255,255,0.06)",
            transition: "all 0.3s ease",
            backdropFilter: "blur(10px)",
            width: "100%",
            boxSizing: "border-box"
          }}>
            <h2 style={{
              color: "#a78bfa",
              fontSize: "18px",
              fontWeight: "600",
              marginBottom: "10px",
              display: "flex",
              alignItems: "center",
              gap: "10px"
            }}>
              <span className="icon" style={{ fontSize: "20px" }}>🚀</span> Future Scope
            </h2>
            {renderValue(analysis.future_scope)}
          </div>
        </div>

        <button 
          className="premium-btn-dark center-btn"
          onClick={() => setPage("upload")}
          style={{
            display: "block",
            margin: "30px auto 0",
            padding: "16px 45px",
            background: "linear-gradient(135deg, #7c3aed, #6d28d9)",
            color: "white",
            border: "none",
            borderRadius: "12px",
            fontSize: "17px",
            fontWeight: "600",
            cursor: "pointer",
            transition: "all 0.3s ease",
            boxShadow: "0 4px 20px rgba(124,58,237,0.25)"
          }}
          onMouseEnter={(e) => {
            e.target.style.transform = "translateY(-2px)";
            e.target.style.boxShadow = "0 8px 35px rgba(124,58,237,0.4)";
          }}
          onMouseLeave={(e) => {
            e.target.style.transform = "translateY(0)";
            e.target.style.boxShadow = "0 4px 20px rgba(124,58,237,0.25)";
          }}
        >
          🔄 Analyze Another Paper
        </button>
      </div>
    </div>
  );
}

export default Result;