# ATS Resume Optimizer

Optimize your resume for any job description using AI (Claude or GPT-4).

## Features

- **AI-Powered Optimization**: Uses Claude or GPT-4 to tailor your resume
- **ATS Keyword Matching**: Extracts and integrates relevant keywords from job descriptions
- **STAR Method**: Restructures achievements using Situation-Task-Action-Result format
- **Writing Quality**: Applies professional writing rules to avoid AI-sounding text
- **Multiple Formats**: Download as Markdown or PDF
- **Privacy First**: Your data is never stored - processed in memory only

## How to Use

1. **Get an API Key**:
   - Claude: [console.anthropic.com](https://console.anthropic.com/)
   - OpenAI: [platform.openai.com](https://platform.openai.com/)

2. **Enter Your Resume**: Paste your current resume or upload a file

3. **Paste Job Description**: Include the full JD with requirements

4. **Click Optimize**: AI will tailor your resume for the specific role

5. **Download**: Get your optimized resume as Markdown or PDF

## Run Locally

```bash
# Clone the repo
git clone https://github.com/yourusername/ats-resume-optimizer.git
cd ats-resume-optimizer

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Deploy!

## Privacy

- **No data storage**: Resumes and JDs are processed in memory only
- **No API key storage**: Your API key is used for a single request and discarded
- **Open source**: Review the code yourself

## Tech Stack

- **Frontend**: Streamlit
- **AI**: Anthropic Claude / OpenAI GPT-4
- **PDF Generation**: fpdf2

## License

MIT License - feel free to use and modify!
