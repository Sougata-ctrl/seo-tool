from flask import Flask, render_template, request
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

PROMPT_TEMPLATE = """
Act as YouTube SEO expert. Create optimized content in this EXACT format:

VIDEO DETAILS:
* Format: {fmt}
* Main Subject: {topic}
* Key Persons: {name}
* Location: {location}
* Brief Context: {event}

REQUIRED OUTPUT FORMAT:

TITLE (80-100 characters):
* Shorts: [Name] | [Bengali Middle] | News | Shorts
* Long: [Name] | [Bengali Middle] | [Category] | News
* Live: Live | [Name] | [Bengali Middle] | News

DESCRIPTION (Exact Structure):
"[Clickbait Quote in Bengali]" | [Context in Bengali] | {category} | Bangla News | West Bengal News
[Bengali journalist article 4-6 sentences]
[English journalist article 4-6 sentences]
[12 hashtags lowercase English only]

TAGS:
Exactly 500 characters, comma-separated, lowercase.

STRICT RULES:
- Title must be 80-100 chars
- Tags must be exactly 500 chars
- 12 hashtags only
- No Bengali in tags
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        topic = request.form.get("topic")
        name = request.form.get("name")
        location = request.form.get("location")
        event = request.form.get("event")
        category = request.form.get("category")
        fmt = request.form.get("format")

        prompt = PROMPT_TEMPLATE.format(
            topic=topic,
            name=name,
            location=location,
            event=event,
            category=category,
            fmt=fmt
        )

        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "You are a strict SEO generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        result = response.choices[0].message.content

        return render_template("index.html", ai_result=result)

    return render_template("index.html") 