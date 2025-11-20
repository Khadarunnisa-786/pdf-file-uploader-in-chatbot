import pathlib
import os
from dotenv import load_dotenv
import google.generativeai as genai

# --- Load API key ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- File path ---
filepath = pathlib.Path("data\what is semisupervised ml.pdf")

# --- Model ---
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Open file and send to model ---
prompt = "Summarize this document"

with open(filepath, "rb") as f:
    response = model.generate_content(
        [prompt, {"mime_type": "application/pdf", "data": f.read()}]
    )

print(response.text)
