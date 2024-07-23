import os

from dotenv import load_dotenv

from routellm.controller import Controller

load_dotenv()

print("Working ... ")
os.environ["GROQ_API_KEY"] = os.getenv('GROQ_API_KEY')
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

client = Controller(
    routers=["mf"],
    strong_model="gpt-3.5-turbo-0125",
    weak_model="groq/llama3-8b-8192",
)

response = client.chat.completions.create(
    model="router-mf-0.11593",
    messages=[
        {"role": "user", "content": "Write a research paper which discusses the use of large language models?"}
    ]
)
print(f"Response: {response.choices[0].message.content}")
print(f"Model: {response.model}")
