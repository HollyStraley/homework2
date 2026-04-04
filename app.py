import anthropic

client = anthropic.Anthropic()

def run_prompt(user_input: str) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    return message.content[0].text

if __name__ == "__main__":
    user_input = input("Enter your prompt: ")
    response = run_prompt(user_input)
    print("\nResponse:")
    print(response)
