
import streamlit as st
import re
from io import BytesIO

# PDF
import PyPDF2

# DOCX
from docx import Document

# PDF Download
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Meeting Minutes Summarizer",
    page_icon="📝",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#1f77b4;
}

.subtitle{
    text-align:center;
    color:gray;
    font-size:18px;
}

.stat-box{
    padding:10px;
    border-radius:10px;
    background-color:#f0f2f6;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<p class="main-title">📝 AI Meeting Minutes Summarizer</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Automatic Meeting Notes Summarization using NLP</p>',
    unsafe_allow_html=True
)

st.divider()

# ==========================================
# SUMMARY FUNCTION
# ==========================================

def generate_summary(text):

    sentences = re.split(r'(?<=[.!?]) +', text)

    if len(sentences) <= 3:
        return text

    summary = " ".join(sentences[:3])

    return summary

# ==========================================
# PDF READER
# ==========================================

def read_pdf(uploaded_file):

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"

    return text

# ==========================================
# DOCX READER
# ==========================================

def read_docx(uploaded_file):

    doc = Document(uploaded_file)

    text = "\n".join(
        [para.text for para in doc.paragraphs]
    )

    return text

# ==========================================
# PDF EXPORT
# ==========================================

def create_pdf(summary_text):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = [
        Paragraph("AI Generated Summary",
                  styles['Title']),
        Paragraph(summary_text,
                  styles['BodyText'])
    ]

    doc.build(content)

    buffer.seek(0)

    return buffer

# ==========================================
# SECTION 1
# ==========================================

st.header("📄 Section 1: Enter Meeting Notes")

meeting_notes = st.text_area(
    "Paste meeting notes here...",
    height=250
)

# ==========================================
# FILE UPLOADS
# ==========================================

st.subheader("📂 Upload Meeting File")

uploaded_file = st.file_uploader(
    "Upload PDF or DOCX",
    type=["pdf", "docx"]
)

if uploaded_file is not None:

    if uploaded_file.name.endswith(".pdf"):

        meeting_notes = read_pdf(uploaded_file)

        st.success("PDF uploaded successfully!")

    elif uploaded_file.name.endswith(".docx"):

        meeting_notes = read_docx(uploaded_file)

        st.success("DOCX uploaded successfully!")

    st.text_area(
        "Extracted Content",
        meeting_notes,
        height=200
    )

# ==========================================
# SECTION 2
# ==========================================

st.header("⚙️ Section 2: Generate Summary")

generate = st.button(
    "Generate Summary"
)

# ==========================================
# PROCESS
# ==========================================

if generate:

    if not meeting_notes.strip():

        st.warning(
            "Please enter meeting notes."
        )

    else:

        summary = generate_summary(
            meeting_notes
        )

        # ==================================
        # SECTION 3
        # ==================================

        st.header(
            "🤖 Section 3: AI Generated Summary"
        )

        st.success(summary)

        # ==================================
        # SECTION 4
        # ==================================

        original_words = len(
            meeting_notes.split()
        )

        summary_words = len(
            summary.split()
        )

        compression_ratio = (
            (original_words - summary_words)
            / original_words
        ) * 100

        st.header(
            "📊 Section 4: Statistics"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Original Words",
                original_words
            )

        with col2:

            st.metric(
                "Summary Words",
                summary_words
            )

        with col3:

            st.metric(
                "Compression Ratio",
                f"{compression_ratio:.2f}%"
            )

        # ==================================
        # CHART
        # ==================================

        st.subheader(
            "Summary Compression"
        )

        st.bar_chart({
            "Words":[
                original_words,
                summary_words
            ]
        })

        # ==================================
        # DOWNLOAD PDF
        # ==================================

        pdf_file = create_pdf(summary)

        st.download_button(

            label="📥 Download Summary as PDF",

            data=pdf_file,

            file_name="meeting_summary.pdf",

            mime="application/pdf"
        )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <center>
    Built with Streamlit • NLP • Deep Learning
    </center>
    """,
    unsafe_allow_html=True
)
