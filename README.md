# ATS Resume Optimizer

Optimize your resume for any job description using AI. Supports multiple LLM providers.

## Features

- **Multi-provider support**: Claude, OpenAI, OpenRouter, Gemini
- **BYOK (Bring Your Own Key)**: Your API key, your control
- **Privacy-first**: No data stored, processed in real-time
- **ATS-optimized**: Keyword matching, STAR method, clean formatting
- **Download options**: Markdown export, clipboard copy

## Live Demo

[ats-resume-optimizer.rashigupta.cloud](https://ats-resume-optimizer.rashigupta.cloud)

## Deploy Your Own

### Vercel (Recommended)

1. Fork this repository
2. Import to Vercel: [vercel.com/new](https://vercel.com/new)
3. Deploy - no environment variables needed!

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/rashis-git/ats-resume-optimizer)

### Local Development

```bash
# Install Vercel CLI
npm i -g vercel

# Run locally
vercel dev
```

## Project Structure

```
ats-resume-optimizer/
├── api/
│   └── optimize.py      # Serverless API endpoint
├── public/
│   └── index.html       # Frontend UI
├── prompts/
│   └── rules.md         # Writing style guidelines
├── requirements.txt     # Python dependencies
└── vercel.json          # Vercel configuration
```

## API Usage

```bash
POST /api/optimize
Content-Type: application/json

{
  "provider": "Claude",
  "api_key": "your-api-key",
  "resume": "# Your resume in markdown...",
  "job_description": "The target job description..."
}
```

## Supported Providers

| Provider | Model | Get API Key |
|----------|-------|-------------|
| Claude | claude-sonnet-4 | [console.anthropic.com](https://console.anthropic.com/) |
| OpenAI | gpt-4o | [platform.openai.com](https://platform.openai.com/) |
| OpenRouter | claude-sonnet-4 | [openrouter.ai](https://openrouter.ai/) |
| Gemini | gemini-1.5-pro | [aistudio.google.com](https://aistudio.google.com/) |

## Privacy

- Your resume and API key are sent directly to the LLM provider
- No data is stored on our servers
- All processing happens in serverless functions with no persistence

## License

MIT
