from openai import OpenAI

MODEL_NAME = "deepseek-r1:8b"
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

respone = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {"rolle": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The LA Dodgers won in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)

print(respone.choices[0].message.content)