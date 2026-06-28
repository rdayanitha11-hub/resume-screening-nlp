# 🤖 NLP Resume Screening Tool

**Live Demo:** https://resume-screening-nlp.onrender.com 

### 🎯 Problem
HR teams spend 6+ hours manually screening resumes for each job posting.

### ✅ Solution  
Automated resume screening using NLP. Upload resume + job description → Get instant match % in 3 seconds.

### 🛠️ Tech Stack
- **Python** | **NLP** | **Streamlit** | **Scikit-learn** | **PyPDF2**
- **TF-IDF Vectorization** + **Cosine Similarity** for matching
- **Deployed on Render**

### 🚀 Key Features
- PDF text extraction from resumes
- Real-time similarity score calculation  
- Clean, responsive web interface
- Supports multiple resume formats

### 📊 How It Works
1. Extract text from uploaded PDF resume
2. Process job description text  
3. Convert both to TF-IDF vectors
4. Calculate cosine similarity score
5. Display match percentage

### 🔧 Run Locally
```bash
git clone https://github.com/rdayanitha11-hub/resume-screening-nlp
pip install -r requirements.txt
streamlit run app.py
