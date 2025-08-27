# Weather→Plan Agent

An intelligent AI agent that creates personalized day plans based on real-time weather conditions. Built with LangChain and powered by Google's Gemini AI, it combines live weather data with smart planning to suggest weather-appropriate activities, safety checklists, and practical tips.

## ✨ Features

- **Real-time Weather Integration** - Fetches live weather data via OpenWeather API
- **Intelligent Planning** - Generates personalized morning/afternoon/evening plans
- **Weather-Aware Suggestions** - Recommends indoor/outdoor activities based on conditions
- **Safety Checklists** - Provides clothing, accessories, and precaution recommendations
- **Kid-Friendly Mode** - Special planning considerations for families with children
- **Multi-language Support** - Responds in the user's preferred language
- **General Knowledge** - Can also answer questions about places, concepts, and topics
- **Dual Interface** - CLI and Streamlit web interface options

## 🏗️ Architecture

- **`app.py`** → Streamlit web interface with chat functionality
- **`agent.py`** → LangChain agent with Gemini AI integration and tool management
- **`tools.py`** → Weather API integration with OpenWeather
- **`prompts/system.txt`** → Intelligent system prompt with decision logic

## 🚀 Setup

1. **Clone and setup:**
```bash
git clone <your-repo>
cd weather-plan-agent-project
python -m venv venv
source venv/bin/activate   # On macOS/Linux
# .\venv\Scripts\activate  # On Windows
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Environment configuration:**
   - Get a [Gemini API key](https://aistudio.google.com/app/apikey) (free)
   - Get an [OpenWeather API key](https://openweathermap.org/api) (free tier available)
   - Create `.env` file:
```env
GEMINI_API_KEY=your_gemini_key_here
OPENWEATHER_API_KEY=your_openweather_key_here
```

4. **Run the app:**
```bash
# Streamlit interface (recommended)
streamlit run app.py

# CLI interface
python app.py
```

## 💡 Usage Examples

- **Weather Planning**: "Plan my day in Barcelona"
- **Family Planning**: "I'm going to Paris with kids, plan our day"
- **General Knowledge**: "Tell me about the Eiffel Tower"
- **Combined Requests**: "What is Central Park and plan my day in New York"

## 🔧 Technical Highlights

- **LangChain Framework** - Modern AI agent architecture
- **Real-time API Integration** - Live weather data processing
- **Intelligent Decision Making** - Context-aware tool usage
- **Error Handling** - Robust API failure management
- **Session Management** - Persistent chat history
- **Responsive UI** - Mobile-friendly Streamlit interface

## 🎯 Portfolio Value

This project demonstrates:
- **AI/LLM Integration** - Working with modern AI frameworks and APIs
- **Full-Stack Development** - Backend logic + frontend interface
- **API Design** - Clean tool interfaces and error handling
- **User Experience** - Intuitive planning assistant
- **Production Practices** - Environment management, dependency handling
- **Problem Solving** - Real-world application of AI for practical use cases

## 🚧 Future Enhancements

- [ ] Multi-city trip planning
- [ ] Historical weather analysis
- [ ] Activity recommendations database
- [ ] Integration with calendar apps
- [ ] Weather alerts and notifications
- [ ] Mobile app version

## 📝 License

MIT License - See License file for details

