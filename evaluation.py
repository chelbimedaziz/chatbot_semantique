from chatbot import answer_question

print("=" * 40)
print("   🤖 AI Knowledge Chatbot (CLI)")
print("=" * 40)
print("Type 'quit' to exit.\n")

while True:
    question = input("You: ").strip()
    if not question:
        continue
    if question.lower() in ["quit", "exit", "bye"]:
        print("Chatbot: Goodbye! 👋")
        break
    response = answer_question(question)
    print(f"Chatbot: {response}\n")