from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import get_weather, get_location

from config import get_gemini_api_key

GEMINI_API_KEY = get_gemini_api_key()
if GEMINI_API_KEY is None:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Please set it in your .env file or Streamlit secrets."
    )

# Tools are plain Python callables; create_agent() in LangChain 1.x wraps them automatically.
tools = [get_weather, get_location]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    api_key=GEMINI_API_KEY,  
)

with open("prompts/system.txt", "r", encoding="utf-8") as file:
    system_prompt = file.read()

agent = create_agent(model=llm, tools=tools, system_prompt=system_prompt)
