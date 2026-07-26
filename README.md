Research Paper Analyser is an AI-powered web application that automatically extracts and analyzes key insights from academic research papers using Natural Language Processing and Machine Learning. Users can upload PDF papers and receive instant structured analysis including title, abstract summary, keywords, methodology, algorithms used, dataset information, results, advantages, and future scope. The application is built with React.js for the frontend, Python FastAPI for the backend, and MongoDB for database storage, featuring a modern glass-morphism user interface with secure user authentication

Features

- Upload Research Papers (PDF format)
- AI-Powered Analysis - Automatic extraction of key insights
- Abstract Summarization - Get concise paper summaries
- Keyword Extraction - Identify important keywords using TF-IDF
- Algorithm Detection - Detect ML algorithms used (CNN, BERT, LSTM, etc.)
- Results Extraction - Extract key findings and performance metrics
- Future Scope - Identify future research directions
- User Authentication - Secure login and registration
- Modern UI - Glass-morphism design with animated background
  
Frontend
- React.js
- Vite
- Lucide React (Icons)
- CSS3 (Glass-morphism, Animations)

Backend
- Python
- FastAPI
- PyPDF (PDF parsing)
- NLP and Machine Learning

 Database
- MongoDB

 How to Run Locally

Prerequisites
- Node.js (v18+)
- Python (v3.8+)
- MongoDB

Step 1: Clone the Repository
git clone https://github.com/Jagadeeswari4/Research-Paper-Analyser.git
cd Research-Paper-Analyser

Step 2: Backend Setup
cd backend
pip install -r requirements.txt,
python -m uvicorn main:app --reload --port 8000,
The backend will run on `http://localhost:8000`

Step 3: Frontend Setup (Open New Terminal)
cd frontend,
npm install,
npm run dev

Step 4: Open in Browser
http://localhost:5173
