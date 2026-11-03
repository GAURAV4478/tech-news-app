import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM = (
    "You summarize tech news. Write 5 short bullet points of what matters "
    "today, in plain simple English. No intro, no outro."
)


def digest(items):
    headlines = "\n".join(f"- {i['title']}" for i in items[:30])
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # check Groq's docs for current model names
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": headlines},
            ],
        )
        return res.choices[0].message.content
    except Exception as e:
        print(f"[ai error] {e}")
        return "AI summary unavailable right now. Headlines below."