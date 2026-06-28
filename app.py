import streamlit as st
import PyPDF2
import io

# Page config
st.set_page_config(
    page_title="AI Resume Screening Tool",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Screening Tool")
st.markdown("Upload multiple resumes and match them against a Job Description")

# Sidebar
st.sidebar.header("📝 Input")

# File uploader
uploaded_files = st.file_uploader(
    "Upload Resumes - PDF only", 
    type="pdf", 
    accept_multiple_files=True,
    help="You can upload multiple PDF files"
)

# Job Description
job_desc = st.text_area(
    "Paste Job Description Here", 
    height=200,
    placeholder="Example: Looking for Python Developer with Flask, AWS experience..."
)

# Check Match Button
if st.button("🔍 Check Match", type="primary"):
    
    # Validation
    if not uploaded_files:
        st.error("⚠️ Please upload at least one resume")
    elif not job_desc.strip():
        st.error("⚠️ Please paste the job description")
    else:
        st.success(f"Processing {len(uploaded_files)} resumes...")
        st.markdown("---")
        
        # JD keywords ah edukuradhu
        jd_words = set(job_desc.lower().split())
        # Stop words ah remove pannu - a, the, and mathiri
        stop_words = {'a', 'an', 'the', 'and', 'or', 'is', 'are', 'with', 'for', 'in', 'to', 'of'}
        jd_keywords = {word.strip('.,()') for word in jd_words if word not in stop_words and len(word) > 2}
        
        # Results store panna list
        results = []
        
        # Loop through each file
        for file in uploaded_files:
            st.subheader(f"📋 Results for: {file.name}")
            
            try:
                # Important: getvalue() use pannanum, read() illa
                pdf_file = io.BytesIO(file.getvalue())
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                
                # Extract text from all pages
                text = ""
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + " "
                
                if not text.strip():
                    st.warning("Could not extract text. This might be a scanned/image PDF")
                    st.write(f"**Match Score: 0.0%**")
                    results.append({"Resume": file.name, "Score": 0})
                else:
                    # Word count
                    word_count = len(text.split())
                    st.write(f"**Word Count:** {word_count}")
                    
                    # Matching logic
                    resume_words = set(text.lower().split())
                    resume_keywords = {word.strip('.,()') for word in resume_words}
                    
                    # Common keywords find pannu
                    matched_keywords = jd_keywords.intersection(resume_keywords)
                    
                    # Score calculate pannu
                    if len(jd_keywords) > 0:
                        score = (len(matched_keywords) / len(jd_keywords)) * 100
                    else:
                        score = 0
                    
                    # Display score with color
                    if score >= 70:
                        st.success(f"**Match Score: {score:.1f}%** - Strong Match ✅")
                    elif score >= 40:
                        st.warning(f"**Match Score: {score:.1f}%** - Average Match ⚠️")
                    else:
                        st.error(f"**Match Score: {score:.1f}%** - Weak Match ❌")
                    
                    # Show matched keywords
                    if matched_keywords:
                        st.write(f"**Matched Skills:** {', '.join(list(matched_keywords)[:10])}")
                    
                    results.append({"Resume": file.name, "Score": score})
                
            except Exception as e:
                st.error(f"Error processing {file.name}: This PDF cannot be read. Use text-based PDF")
                results.append({"Resume": file.name, "Score": 0})
            
            st.markdown("---")
        
        # Final ranking
        if results:
            st.subheader("🏆 Final Ranking")
            results_sorted = sorted(results, key=lambda x: x['Score'], reverse=True)
            for i, res in enumerate(results_sorted, 1):
                st.write(f"{i}. **{res['Resume']}** - {res['Score']:.1f}%")

else:
    st.info("👈 Upload resumes and paste JD, then click 'Check Match'")

# Footer
st.markdown("---")
st.caption("Built with Python + Streamlit + PyPDF2 | NLP Resume Screening")