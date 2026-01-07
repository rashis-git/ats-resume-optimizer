"""
ATS Resume Optimizer - Vercel Serverless API
POST /api/optimize
"""

import json
from http.server import BaseHTTPRequestHandler
from pathlib import Path


def get_system_prompt():
    """Load the ATS system prompt with writing rules"""
    # In Vercel, the file path is relative to the project root
    rules_path = Path(__file__).parent.parent / "prompts" / "rules.md"

    if rules_path.exists():
        rules = rules_path.read_text(encoding='utf-8')
    else:
        rules = ""

    system_prompt = f"""You are an expert ATS (Applicant Tracking System) Resume Optimizer. Your task is to tailor a candidate's resume for a specific job description.

## Your Process:

1. **Analyze the Job Description:**
   - Extract must-have keywords (mentioned 3+ times or in requirements)
   - Extract should-have keywords (mentioned 1-2 times or preferred)
   - Identify the primary role focus and responsibilities

2. **Tailor the Resume:**
   - Rewrite the Professional Summary to match the role positioning
   - Reorder experience bullets to prioritize JD-relevant achievements
   - Integrate keywords naturally (no keyword stuffing)
   - Use the STAR method: Situation, Task, Action, Result
   - Ensure all achievements are quantified where possible

3. **Apply Writing Rules:**
   - Follow all banned words and phrases listed below
   - Vary sentence lengths (short-long-short pattern)
   - Be specific with numbers, not vague praise
   - Pass the "coffee test" - would you say this to a colleague?

## Writing Rules:
{rules}

## Output Format:
Return the optimized resume in clean markdown format with:
- Name and contact info at top
- Clear section headers (PROFESSIONAL SUMMARY, EXPERIENCE, PROJECTS, EDUCATION, SKILLS, CERTIFICATIONS)
- Bullet points for achievements
- Bold for company names and role titles

After the resume, provide a brief "Changes Summary" section explaining:
- Key changes made
- Keywords integrated
- ATS keyword coverage estimate
"""
    return system_prompt


def optimize_with_claude(api_key: str, resume: str, job_description: str) -> str:
    """Optimize resume using Claude API"""
    from anthropic import Anthropic

    client = Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=get_system_prompt(),
        messages=[
            {
                "role": "user",
                "content": f"""Please optimize this resume for the following job description.

## Current Resume:
{resume}

## Job Description:
{job_description}

Please return the optimized resume in markdown format, followed by a changes summary."""
            }
        ]
    )

    return message.content[0].text


def optimize_with_openai(api_key: str, resume: str, job_description: str) -> str:
    """Optimize resume using OpenAI API"""
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=4096,
        messages=[
            {
                "role": "system",
                "content": get_system_prompt()
            },
            {
                "role": "user",
                "content": f"""Please optimize this resume for the following job description.

## Current Resume:
{resume}

## Job Description:
{job_description}

Please return the optimized resume in markdown format, followed by a changes summary."""
            }
        ]
    )

    return response.choices[0].message.content


def optimize_with_openrouter(api_key: str, resume: str, job_description: str) -> str:
    """Optimize resume using OpenRouter API"""
    from openai import OpenAI

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    response = client.chat.completions.create(
        model="anthropic/claude-sonnet-4",
        max_tokens=4096,
        messages=[
            {
                "role": "system",
                "content": get_system_prompt()
            },
            {
                "role": "user",
                "content": f"""Please optimize this resume for the following job description.

## Current Resume:
{resume}

## Job Description:
{job_description}

Please return the optimized resume in markdown format, followed by a changes summary."""
            }
        ]
    )

    return response.choices[0].message.content


def optimize_with_gemini(api_key: str, resume: str, job_description: str) -> str:
    """Optimize resume using Google Gemini API"""
    import google.generativeai as genai

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-1.5-pro')

    prompt = f"""{get_system_prompt()}

Please optimize this resume for the following job description.

## Current Resume:
{resume}

## Job Description:
{job_description}

Please return the optimized resume in markdown format, followed by a changes summary."""

    response = model.generate_content(prompt)

    return response.text


def optimize_resume(provider: str, api_key: str, resume: str, job_description: str) -> str:
    """Main function to optimize resume using selected LLM provider"""
    if provider == "Claude":
        return optimize_with_claude(api_key, resume, job_description)
    elif provider == "OpenAI":
        return optimize_with_openai(api_key, resume, job_description)
    elif provider == "OpenRouter":
        return optimize_with_openrouter(api_key, resume, job_description)
    elif provider == "Gemini":
        return optimize_with_gemini(api_key, resume, job_description)
    else:
        raise ValueError(f"Unknown provider: {provider}")


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Extract parameters
            provider = data.get('provider', 'Claude')
            api_key = data.get('api_key', '')
            resume = data.get('resume', '')
            job_description = data.get('job_description', '')

            # Validate
            if not api_key:
                self._send_error(400, "API key is required")
                return
            if not resume:
                self._send_error(400, "Resume text is required")
                return
            if not job_description:
                self._send_error(400, "Job description is required")
                return

            # Optimize
            optimized = optimize_resume(provider, api_key, resume, job_description)

            # Send response
            self._send_response(200, {"success": True, "optimized_resume": optimized})

        except Exception as e:
            self._send_error(500, str(e))

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def _send_error(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps({"success": False, "error": message}).encode('utf-8'))
