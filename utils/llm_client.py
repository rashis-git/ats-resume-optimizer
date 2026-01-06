"""
LLM Client for ATS Resume Optimizer
Supports both Claude (Anthropic) and OpenAI APIs
"""

from pathlib import Path


def get_system_prompt():
    """Load the ATS system prompt with writing rules"""
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
    try:
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

    except Exception as e:
        raise Exception(f"Claude API Error: {str(e)}")


def optimize_with_openai(api_key: str, resume: str, job_description: str) -> str:
    """Optimize resume using OpenAI API"""
    try:
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

    except Exception as e:
        raise Exception(f"OpenAI API Error: {str(e)}")


def optimize_with_openrouter(api_key: str, resume: str, job_description: str) -> str:
    """Optimize resume using OpenRouter API"""
    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )

        response = client.chat.completions.create(
            model="anthropic/claude-sonnet-4",  # Can use any model on OpenRouter
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

    except Exception as e:
        raise Exception(f"OpenRouter API Error: {str(e)}")


def optimize_with_gemini(api_key: str, resume: str, job_description: str) -> str:
    """Optimize resume using Google Gemini API"""
    try:
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

    except Exception as e:
        raise Exception(f"Gemini API Error: {str(e)}")


def optimize_resume(provider: str, api_key: str, resume: str, job_description: str) -> str:
    """
    Main function to optimize resume using selected LLM provider

    Args:
        provider: "Claude", "OpenAI", "OpenRouter", or "Gemini"
        api_key: User's API key
        resume: The resume text to optimize
        job_description: The target job description

    Returns:
        Optimized resume in markdown format
    """
    if not api_key:
        raise ValueError("API key is required")

    if not resume:
        raise ValueError("Resume text is required")

    if not job_description:
        raise ValueError("Job description is required")

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
