import os
from dotenv import load_dotenv
from parsera import Parsera

url = "https://www.jordanmungujakisa.com/"

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

elements = {
    "headline": "The headline of the page",
    "description": "The description of the page",
    "projects": "The projects that the person has done.",
    "faqs": "The frequently asked questions"
}

results = Parsera().run(url, elements)
print(results)