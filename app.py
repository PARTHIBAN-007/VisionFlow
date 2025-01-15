import os
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import streamlit.components.v1 as components

# Load environment variables
API_KEY = os.getenv("GOOGLE_API_KEY")


def configure_genai() -> bool:
    """Configure Google Generative AI with the provided API key."""
    if not API_KEY:
        st.error("API Key is not found. Please set a valid Google API key.")
        return False
    try:
        genai.configure(api_key=API_KEY)
        return True
    except Exception as e:
        st.error(f"Error in API configuration: {str(e)}")
        return False


def extract_text(pdf_file) -> str:
    """Extract text from the uploaded PDF file."""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if not text.strip():
            st.warning("No text could be extracted from the PDF. Please upload a valid text-based PDF.")
            return ""
        return text.strip()
    except Exception as e:
        st.error(f"Error reading the PDF file: {str(e)}")
        return ""


def mindmap_keyword(text) -> str:
    """Generate hierarchical Markdown for a mindmap using Gemini AI."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        max_chars = 300000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
            st.warning(f"Text truncated to {max_chars} characters due to LLM restrictions.")
        
        prompt = f"""
        Create a hierarchical Markdown mindmap from the following text:
        Use proper Markdown heading syntax (# for main topics, ## for subtopics, ### for details).
        Focus on the main concepts and their relationships.
        Text to analyze: {text}
        Respond only with the Markdown mindmap.
        """
        response = model.generate_content(prompt)
        if not response.text or not response.text.strip():
            st.error("No response received from LLM.")
            return ""
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating mindmap: {str(e)}")
        return ""


def create_mindmap(markdown_content):
    """Generate interactive mindmap HTML from Markdown."""
    markdown_content = markdown_content.replace("`", "\\`").replace("${", "\\${")
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            #mindmap {{
                width: 100%;
                height: 600px;
                background-color: #e5e5e5;
                border-radius: 25px;
            }}
        </style>
        <script src="https://cdn.jsdelivr.net/npm/d3@6"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-view"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-lib@0.14.3/dist/browser/index.min.js"></script>
    </head>
    <body>
        <svg id="mindmap"></svg>
        <script>
            window.onload = () => {{
                const markdown = `{markdown_content}`;
                const transformer = new markmap.Transformer();
                const {{ root }} = transformer.transform(markdown);
                const mm = new markmap.Markmap(document.querySelector('#mindmap'), {{
                    maxWidth: 600,
                    color: (node) => {{
                        const level = node.depth;
                        return ['#2196f3', '#4caf50', '#ff9800', '#f44336'][level % 4];
                    }},
                    paddingX: 16,
                    autoFit: true,
                    initialExpandLevel: 2,
                    duration: 500,
                }});
                mm.setData(root);
                mm.fit();
            }};
        </script>
    </body>
    </html>
    """
    return html_content


def main():
    """Main function to handle file upload, mindmap generation, and visualization."""
    st.set_page_config(layout="wide")
    st.title("📚 Vision Flow")
    st.markdown("Convert PDFs to interactive, editable mindmaps using AI.")

    if not configure_genai():
        return

    uploaded_file = st.file_uploader("Upload a PDF file:", type="pdf")

    if uploaded_file is not None:
        with st.spinner("Processing the uploaded PDF..."):
            text = extract_text(uploaded_file)

        if text:
            st.success("Text in PDF is successfully extracted.")

            if "markdown_content" not in st.session_state:
                st.session_state.markdown_content = mindmap_keyword(text)

            tab1, tab2 = st.tabs(["📊 Mindmap", "📝 Markdown Editor"])

            with tab1:
                st.subheader("Interactive Mindmap")
                html_content = create_mindmap(st.session_state.markdown_content)
                components.html(html_content, height=700, scrolling=True)

            with tab2:
                st.subheader("Edit Markdown")
                edited_markdown = st.text_area(
                    "Modify the Markdown below to update the mindmap:",
                    value=st.session_state.markdown_content,
                    height=400,
                )
                
                st.success("Markdown updated!")
                html_content = create_mindmap(edited_markdown)
                components.html(html_content, height=700, scrolling=True)

main()
