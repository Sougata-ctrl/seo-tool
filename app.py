from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

PROMPT_TEMPLATE = """
Act as YouTube SEO expert.

Create optimized content in EXACT format:

VIDEO DETAILS:
* Format: Long
* Main Subject: WB Election 2026
* Key Persons: {name}
* Location: West Bengal
* Brief Context: {event}

REQUIRED OUTPUT FORMAT:

TITLE (80-100 characters):
{Name} | "..." — ... | Bengal Politics | News

DESCRIPTION:
"..." | ... | Bengal Politics | Bangla News | West Bengal News
[Bangla article 4-6 sentences]
[English article 4-6 sentences]
[12 hashtags lowercase]

TAGS:
Exactly 500 characters, comma-separated lowercase
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        event = request.form["event"]

        prompt = PROMPT_TEMPLATE.format(name=name, event=event)

        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": prompt}]
        )

        output = response.choices[0].message.content

        return render_template("index.html", result=output)

    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run()
