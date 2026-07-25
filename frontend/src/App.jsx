import React from "react";
import { useState } from "react";
import Login from "./pages/Login";
import Upload from "./pages/Upload";
import Result from "./pages/Result";

function App() {
  const [page, setPage] = useState("login");
  const [analysis, setAnalysis] = useState(null);

  return (
    <div>
      {page === "login" && <Login setPage={setPage} />}
      {page === "upload" && (
        <Upload setPage={setPage} setAnalysis={setAnalysis} />
      )}
      {page === "result" && <Result analysis={analysis} setPage={setPage} />}
    </div>
  );
}

export default App;