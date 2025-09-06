[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://laurapuerto-weather-plan.streamlit.app/)


# Weather->Plan Agent

An intelligent AI agent that creates personalized day plans based on real-time weather conditions.  
Built with **LangChain** and powered by **Google's Gemini AI**, it combines live weather data with smart planning to suggest weather-appropriate activities, safety checklists, and practical tips.  

---

## ✨ Features

- **Real-time Weather Integration** – Fetches live weather data via OpenWeather API  
- **Intelligent Planning** – Generates personalized morning/afternoon/evening plans  
- **Weather-Aware Suggestions** – Recommends indoor/outdoor activities based on conditions  
- **Safety Checklists** – Provides clothing, accessories, and precaution recommendations  
- **Kid-Friendly Mode** – Special planning considerations for families with children  
- **Multi-language Support** – Responds in the user’s preferred language  
- **General Knowledge** – Can also answer questions about places, concepts, and topics  
- **Streamlit Web Interface** – Clean, responsive, and mobile-friendly UI  

---

## 🏗️ Architecture

- **`app.py`** – Streamlit web interface with chat and forecast visualization
- **`agent.py`** – LangChain ReAct agent with Gemini AI integration and tool management  
- **`tools.py`** – Weather API integration with OpenWeather (wrapped as LangChain tool)
- **`weather_service.py`** – Low-level functions for current weather and forecast data
- **`config.py`** – Environment-agnostic API key management (local + cloud)
- **`prompts/system.txt`** – System prompt with decision logic for planning
- **`ui/`** – Modular UI components (panels, styles)  

---

## 🚀 Quick Start

1. **Clone the repo and install dependencies**
2. **Get API keys** (Gemini + OpenWeather)  
3. **Create `.env` file** with your keys
4. **Run `streamlit run app.py`**
5. **Ask**: *"Plan my day in Barcelona"*

---

## 🚀 Setup

1. **Clone and setup:**  
```bash
git clone <your-repo>
cd weather-plan-agent-project
python -m venv venv
source venv/bin/activate   # macOS/Linux
# .\venv\Scripts\activate  # Windows
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

4. **Run the app locally:**  
```bash
streamlit run app.py
```

---

## 💡 Usage Examples

- **Weather Planning**: *"Plan my day in Barcelona"*  
- **Family Planning**: *"I'm going to Paris with kids, plan our day"*  
- **General Knowledge**: *"Tell me about the Eiffel Tower"*  
- **Combined Requests**: *"What is Central Park and plan my day in New York"*  

---

## 🔧 Technical Highlights

- **LangChain Framework** – Modern AI agent architecture  
- **Gemini LLM Integration** – Tool-calling and reasoning with Google's generative models  
- **Real-time API Integration** – Live weather data processing via OpenWeather  
- **Error Handling** – Robust API failure management  
- **Session Management** – Persistent chat history with Streamlit session state  
- **Responsive Visualization** – Interactive forecast charts with Plotly  

---

## 🎯 Portfolio Value

This project demonstrates:  
- **AI/LLM Integration** – Practical use of LangChain with Gemini for reasoning and tool calling  
- **End-to-End Application** – From backend logic to a deployed interactive web app  
- **API Design** – Clean tool interfaces and exception handling  
- **User Experience** – Conversational interface with weather visualization  
- **Deployment Practices** – Streamlit Cloud deployment with pinned dependencies  
- **Problem Solving** – Real-world AI applied to daily-life planning  

---

## 📝 License

MIT License – See [LICENSE](LICENSE) file for details  
