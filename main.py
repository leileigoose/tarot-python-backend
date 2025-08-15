from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel

app = FastAPI()

# Allow frontend call backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://quicktarot.onrender.com"], # ["*"], # Uncomment for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample tarot card data
with open("cards.json", "r") as f:
    cards = json.load(f)

# Open AI client setup
print("Opening client")
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Question request model
class QuestionRequest(BaseModel):
    question: str | None = None
    
# Route to get a random card and return summary
@app.get("/draw-card")
def draw_card():
    card = random.choice(cards)
    summary = None

    return {
        "card": card,
        "summary": summary
    }

@app.post("/get-reading")
def get_reading(data: QuestionRequest):
    if data.question:
        card = random.choice(cards)
        prompt = (
            f"My question is {data.question}."
            f"I pulled a {card['card_no']} {card['name']} in the {card['orientation']} position. "
            f"Can you give me a summary of the card meaning of {card['meaning']}  in relation to my question?"
            f"Do not repeat the question or card info, just the summary."
        )

        # Use OpenAI to generate a response based on the question
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        summary = response.choices[0].message.content
    else:
        card = None
        summary = None

    return {
        "card": card,
        "summary": summary
    }
