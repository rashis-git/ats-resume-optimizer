"""
ATS Resume Optimizer - Streamlit Web App
Optimize your resume for any job description using AI
"""

import streamlit as st
from utils.llm_client import optimize_resume
from utils.pdf_generator import create_pdf_bytes

# Page config
st.set_page_config(
    page_title="ATS Resume Optimizer",
    page_icon="📄",
    layout="wide"
)

# Header
st.title("📄 ATS Resume Optimizer")
st.markdown("""
Optimize your resume for any job description using AI.
Your data is processed in real-time and **never stored**.
""")

st.divider()

# Sidebar for API configuration
with st.sidebar:
    st.header("🔑 API Configuration")

    llm_provider = st.selectbox(
        "Select AI Provider",
        ["Claude (Anthropic)", "OpenAI (GPT-4)", "OpenRouter", "Gemini (Google)"],
        help="Choose which AI to use for optimization"
    )

    api_key = st.text_input(
        "API Key",
        type="password",
        help="Your API key is used only for this session and never stored"
    )

    # Map display name to internal name
    provider_map = {
        "Claude (Anthropic)": "Claude",
        "OpenAI (GPT-4)": "OpenAI",
        "OpenRouter": "OpenRouter",
        "Gemini (Google)": "Gemini"
    }

    st.divider()

    st.markdown("""
    ### How to get an API key:
    - **Claude**: [console.anthropic.com](https://console.anthropic.com/)
    - **OpenAI**: [platform.openai.com](https://platform.openai.com/)
    - **OpenRouter**: [openrouter.ai](https://openrouter.ai/)
    - **Gemini**: [aistudio.google.com](https://aistudio.google.com/)

    ### Privacy:
    - Your resume is processed in memory only
    - API key is never stored
    - No data is saved after your session
    """)

# Main content - two columns
col1, col2 = st.columns(2)

with col1:
    st.header("📝 Your Resume")

    # Option to paste or upload
    input_method = st.radio(
        "Input method:",
        ["Paste text", "Upload file"],
        horizontal=True
    )

    if input_method == "Paste text":
        resume_text = st.text_area(
            "Paste your resume here",
            height=400,
            placeholder="# Your Name\nemail@example.com | LinkedIn | Phone\n\n## PROFESSIONAL SUMMARY\n..."
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload resume",
            type=["txt", "md"],
            help="Upload a .txt or .md file"
        )
        if uploaded_file:
            resume_text = uploaded_file.read().decode('utf-8')
            st.text_area("Resume content:", resume_text, height=300, disabled=True)
        else:
            resume_text = ""

with col2:
    st.header("💼 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=400,
        placeholder="Paste the full job description including:\n- Company name\n- Role title\n- Responsibilities\n- Requirements\n- Preferred qualifications"
    )

st.divider()

# Process button
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    process_btn = st.button(
        "🚀 Optimize Resume",
        type="primary",
        use_container_width=True
    )

# Process and show results
if process_btn:
    # Validation
    if not api_key:
        st.error("Please enter your API key in the sidebar")
    elif not resume_text:
        st.error("Please provide your resume")
    elif not job_description:
        st.error("Please provide the job description")
    else:
        # Process
        with st.spinner("Optimizing your resume... This may take 30-60 seconds."):
            try:
                provider = provider_map[llm_provider]
                optimized_resume = optimize_resume(
                    provider=provider,
                    api_key=api_key,
                    resume=resume_text,
                    job_description=job_description
                )

                st.success("Resume optimized successfully!")

                # Show results
                st.header("✨ Optimized Resume")

                # Tabs for different views
                tab1, tab2 = st.tabs(["📄 Preview", "📝 Markdown"])

                with tab1:
                    st.markdown(optimized_resume)

                with tab2:
                    st.code(optimized_resume, language="markdown")

                # Download buttons
                st.divider()
                st.subheader("📥 Download")

                dl_col1, dl_col2, dl_col3 = st.columns([1, 1, 1])

                with dl_col1:
                    st.download_button(
                        label="Download Markdown",
                        data=optimized_resume,
                        file_name="optimized_resume.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

                with dl_col2:
                    try:
                        pdf_bytes = create_pdf_bytes(optimized_resume)
                        if pdf_bytes and len(pdf_bytes) > 0:
                            st.download_button(
                                label="Download PDF",
                                data=pdf_bytes,
                                file_name="optimized_resume.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        else:
                            st.warning("PDF generation returned empty result")
                    except Exception as e:
                        st.error(f"PDF generation failed: {str(e)}")

            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    Built with Streamlit | Your data is never stored
</div>
""", unsafe_allow_html=True)
