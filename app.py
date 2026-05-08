
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import PyPDF2

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content

    return text
def generate_summary(text, sentence_count=10):

    parser = PlaintextParser.from_string(
        text,
        Tokenizer("english")
    )

    summarizer = TextRankSummarizer()

    summary = summarizer(
        parser.document,
        sentence_count
    )

    final_summary = ""

    for sentence in summary:
        final_summary += str(sentence) + " "

    return final_summary
import streamlit as st

st.set_page_config(
    page_title="REVISE AI",
    page_icon="🧠",
    layout="centered"
)

# Title
st.title("🧠 REVISE AI")
st.markdown("### 📚 Smart  Study Summary  Assistant for Students")

st.write("✨ Upload your study material or paste text below to generate quick revision notes.")

# Upload PDF
uploaded_file = st.file_uploader(
    "📄 Upload a PDF File",
    type=["pdf"]
)

# Text input
text_input = st.text_area(
    "📝 Or Paste Your Notes/Text Here"
)

# Summary length
summary_length = st.number_input(
    "📏 Number of Summary Sentences",
    min_value=1,
    value=5,
    step=1,
    help="Choose how many sentences you want in the summary"
)

# Submit button
if st.button("🚀 Generate Summary"):

    final_text = ""

    if uploaded_file is not None:

        final_text = extract_text_from_pdf(uploaded_file)

        st.success("✅ PDF uploaded successfully!")

    elif text_input:

        final_text = text_input

        st.success("✅ Text received successfully!")

    else:

        st.warning("⚠️ Please upload a PDF or enter text.")

    if final_text:

        st.subheader("📝 AI Generated Short Notes")

        with st.spinner("🤖 Generating smart summary..."):

            summary = generate_summary(
                final_text,
                sentence_count=summary_length,
            )

        st.success("🎉 Summary Generated Successfully!")

        st.write(summary)

        st.success("🎉 Summary Generated Successfully!")
        st.toast("✨ Your notes are ready!")
        st.download_button(
        "📥 Download Summary",
        summary,
       file_name="summary.txt"
)