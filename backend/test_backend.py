from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Test Backend Running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # Save the file
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Return simple response
    return {
        "title": f"File: {file.filename}",
        "authors": "Test Author",
        "publication_year": "2024",
        "research_domain": "Testing",
        "abstract_summary": "This is a test summary",
        "keywords": ["test", "keywords"],
        "methodology": "Test methodology",
        "algorithms_used": "Test algorithms",
        "dataset_information": "Test dataset",
        "results": "Test results",
        "limitations": "Test limitations",
        "future_scope": "Test future scope"
    }