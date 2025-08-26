from langchain_core.messages import HumanMessage, AIMessage
from agent import agent_executor

history = []

def main():
    print("Weather→Plan Agent (v0.1)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Bye!")
            break
        response = agent_executor.invoke({"input": user_input, "history": history})
        print(response["output"])
        history.append(HumanMessage(user_input))
        history.append(AIMessage(response["output"]))

if __name__ == "__main__":
    main()
