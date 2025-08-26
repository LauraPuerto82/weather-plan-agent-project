# Weather→Plan Agent

A simple LangChain-powered agent that:  
- Uses a tool (`get_weather`) to retrieve weather information  
- Suggests a basic plan and checklist based on the weather  
- Runs on **Gemini** (Google AI Studio API) for reasoning and responses  
- Currently uses a mock weather tool (no real API calls yet)

## Project Structure
- `app.py` → Main entry point (interactive chat loop)
- `agent.py` → Agent definition, prompt, and Gemini setup
- `tools.py` → Utility tools (mock `get_weather` function)

## Setup

1. **Create a virtual environment** (optional but recommended):
```bash
python -m venv .venv
source .venv/bin/activate   # On macOS/Linux
# .\.venv\Scripts\activate  # On Windows
```

2. **Install dependencies:**
```bash
pip install langchain langchain-google-genai python-dotenv
```

3. **Get a Gemini API key:**
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a free API key (no credit card required)
   - Add it to a `.env` file:
```env
GEMINI_API_KEY=your_api_key_here
```

4. **Run the app:**
```bash
python app.py
```

## Next Steps
- Implement a real OpenWeather API call  
- Improve prompt logic and planning features  
- Add a `kids-friendly` mode