# AI Assistant Chat

A modern, secure chat interface for AI assistants built with Streamlit.

## Features

- 🎨 Clean, Claude-like interface
- 🔒 Secure configuration using Streamlit secrets
- 💬 Real-time chat interactions
- 📱 Responsive design

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-chat-app.git
cd ai-chat-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.streamlit/secrets.toml` file:
```toml
CREATOR_NAME = "Your Name"
MODEL_NAME = "Your AI Name"
OPENROUTER_API_KEY = "your-api-key-here"
MODEL_ID = "meta-llama/llama-3.1-8b-instruct:free"
```

4. Run the app:
```bash
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push your code to GitHub (don't include secrets.toml)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. In the app settings, add your secrets:
   - Go to "Advanced settings" → "Secrets"
   - Paste your configuration in TOML format:

```toml
CREATOR_NAME = "Your Name"
MODEL_NAME = "Your AI Name"
OPENROUTER_API_KEY = "sk-or-v1-xxxxx"
MODEL_ID = "meta-llama/llama-3.1-8b-instruct:free"
```

5. Deploy!

## Get OpenRouter API Key

1. Sign up at [OpenRouter](https://openrouter.ai/)
2. Go to [Keys](https://openrouter.ai/keys)
3. Create a new API key
4. Use free models like:
   - `meta-llama/llama-3.1-8b-instruct:free`
   - `google/gemini-flash-1.5:free`
   - `mistralai/mistral-7b-instruct:free`

## Security

- ✅ API keys stored securely in Streamlit secrets
- ✅ No sensitive data in code
- ✅ Environment variables not exposed
- ✅ Safe for public GitHub repositories

## License

MIT
