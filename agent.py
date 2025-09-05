from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_tools_agent, AgentExecutor
from tools import get_weather
from langchain_google_genai import ChatGoogleGenerativeAI
from config import get_gemini_api_key

GEMINI_API_KEY = get_gemini_api_key()

tools = [get_weather]

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.3,
)

with open("prompts/system.txt", "r", encoding="utf-8") as file:
    system_prompt = file.read()

prompt = ChatPromptTemplate([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,
    return_intermediate_steps=True
)
