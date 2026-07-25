import os
import shutil
import time
import re
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from builtins import Exception,open,print,range,len,str,any,isinstance,list
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI(title="Research Paper Analyzer API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "http://localhost:5176",
        "http://127.0.0.1:5176",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {
        "message": "Research Paper Analyzer Running",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time()
    }

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    start_time = time.time()
    file_path = None
    
    try:
        if not file.filename.endswith('.pdf'):
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Please upload a PDF file.",
                    "title": "Error",
                    "authors": "N/A",
                    "publication_year": "N/A",
                    "research_domain": "N/A",
                    "abstract_summary": "Invalid file type. Please upload a PDF.",
                    "keywords": [],
                    "methodology": "N/A",
                    "algorithms_used": "N/A",
                    "dataset_information": "N/A",
                    "results": "N/A",
                    "advantages": "N/A",
                    "future_scope": "N/A",
                    "processing_time": f"{time.time() - start_time:.2f}s"
                }
            )
        
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"✅ File saved: {file.filename}")
        
        try:
            from pdf_reader import extract_text
            text = extract_text(file_path)
            print(f"✅ Extracted {len(text)} characters")
        except Exception as e:
            print(f"❌ PDF extraction error: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": f"Failed to extract text from PDF: {str(e)}",
                    "title": "Error",
                    "authors": "N/A",
                    "publication_year": "N/A",
                    "research_domain": "N/A",
                    "abstract_summary": "Could not extract text from this PDF.",
                    "keywords": [],
                    "methodology": "N/A",
                    "algorithms_used": "N/A",
                    "dataset_information": "N/A",
                    "results": "N/A",
                    "advantages": "N/A",
                    "future_scope": "N/A",
                    "processing_time": f"{time.time() - start_time:.2f}s"
                }
            )
        
        if len(text) < 100:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Could not extract enough text from PDF.",
                    "title": "Error",
                    "authors": "N/A",
                    "publication_year": "N/A",
                    "research_domain": "N/A",
                    "abstract_summary": "Could not extract enough text.",
                    "keywords": [],
                    "methodology": "N/A",
                    "algorithms_used": "N/A",
                    "dataset_information": "N/A",
                    "results": "N/A",
                    "advantages": "N/A",
                    "future_scope": "N/A",
                    "processing_time": f"{time.time() - start_time:.2f}s"
                }
            )
        
        try:
            from analyzer import analyze_paper
            analysis = analyze_paper(text)
            print(f"✅ Analysis complete")
        except Exception as e:
            print(f"❌ Analysis error: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": f"Analysis failed: {str(e)}",
                    "title": "Error",
                    "authors": "N/A",
                    "publication_year": "N/A",
                    "research_domain": "N/A",
                    "abstract_summary": "An error occurred during analysis.",
                    "keywords": [],
                    "methodology": "N/A",
                    "algorithms_used": "N/A",
                    "dataset_information": "N/A",
                    "results": "N/A",
                    "advantages": "N/A",
                    "future_scope": "N/A",
                    "processing_time": f"{time.time() - start_time:.2f}s"
                }
            )
        
        if "abstract_summary" not in analysis or analysis["abstract_summary"] == "Abstract not found":
            try:
                from summarizer import generate_summary
                analysis["abstract_summary"] = generate_summary(text)
            except Exception as e:
                print(f"⚠️ Summary generation error: {str(e)}")
                analysis["abstract_summary"] = "Summary generation failed."
        
        if "keywords" not in analysis or analysis["keywords"] == "Keywords not found":
            try:
                from keyword_extractor import extract_keywords
                keywords = extract_keywords(text)
                analysis["keywords"] = keywords if keywords else ["Keywords not found"]
            except Exception as e:
                print(f"⚠️ Keyword extraction error: {str(e)}")
                analysis["keywords"] = ["Keywords not found"]
        
        analysis["processing_time"] = f"{time.time() - start_time:.2f}s"
        analysis = clean_analysis_output(analysis)
        
        if "limitations" in analysis:
            del analysis["limitations"]
        
        print(f"✅ Analysis complete in {analysis['processing_time']}")
        return analysis
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": f"Unexpected error: {str(e)}",
                "title": "Error",
                "authors": "N/A",
                "publication_year": "N/A",
                "research_domain": "N/A",
                "abstract_summary": "An unexpected error occurred.",
                "keywords": [],
                "methodology": "N/A",
                "algorithms_used": "N/A",
                "dataset_information": "N/A",
                "results": "N/A",
                "advantages": "N/A",
                "future_scope": "N/A",
                "processing_time": f"{time.time() - start_time:.2f}s"
            }
        )
    finally:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️ Cleaned up: {file_path}")
            except Exception as e:
                print(f"⚠️ Could not delete file: {str(e)}")

def clean_analysis_output(analysis):
    fixes = [
        ('speechrecognition', 'speech recognition'),
        ('recognation', 'recognition'),
        ('recognotion', 'recognition'),
        ('recognitionin', 'recognition in'),
        ('robotsand', 'robots and'),
        ('robustspeech', 'robust speech'),
        ('futuredirections', 'future directions'),
        ('multimodalinter', 'multimodal interaction'),
        ('sysystems', 'systems'),
        ('outlinethechallenges', 'outline the challenges'),
        ('deployingrobust', 'deploying robust'),
        ('discussfuture', 'discuss future'),
    ]
    
    for key, value in analysis.items():
        if isinstance(value, str):
            for wrong, correct in fixes:
                value = value.replace(wrong, correct)
            value = re.sub(r'(\w+)(recognition)', r'\1 recognition', value)
            value = re.sub(r'(\w+)(robots)', r'\1 robots', value)
            value = re.sub(r'(\w+)(discuss)', r'\1 discuss', value)
            value = re.sub(r'(\w+)(future)', r'\1 future', value)
            value = re.sub(r'(\w+)(speech)', r'\1 speech', value)
            value = re.sub(r'\s+', ' ', value)
            analysis[key] = value
        elif isinstance(value, list):
            cleaned_list = []
            for item in value:
                if isinstance(item, str):
                    for wrong, correct in fixes:
                        item = item.replace(wrong, correct)
                    item = re.sub(r'\s+', ' ', item)
                    cleaned_list.append(item)
                else:
                    cleaned_list.append(item)
            analysis[key] = cleaned_list
    
    return analysis

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)