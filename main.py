from llm import LLM

def main():
    llm = LLM()

    while True:
        prompt = input("\nYou: ")
        if prompt.lower() in ["exit", "quit"]:
            break
        response = llm.generate(prompt)
        print(f"\nAssistant:\n{response}")

if __name__ == "__main__":
    main()