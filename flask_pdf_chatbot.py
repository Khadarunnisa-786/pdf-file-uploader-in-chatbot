from flask import Flask, request, jsonify
import tempfile
import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- Load .env variables ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY not found in environment variables or .env")

# --- Configure Gemini ---
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Flask app setup ---
app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_pdf():
    """
    POST /process
    Form-data:
      - pdf_file: PDF file
      - prompt: text prompt or question
    """
    try:
        # --- Validate inputs ---
        if "pdf_file" not in request.files:
            return jsonify({"error": "No PDF file uploaded"}), 400

        prompt = request.form.get("prompt", "").strip()
        if not prompt:
            return jsonify({"error": "Please provide a text prompt"}), 400

        pdf_file = request.files["pdf_file"]

        # --- Save PDF temporarily ---
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf_file.save(tmp_file.name)
            pdf_path = tmp_file.name

        # --- Read bytes and send to Gemini ---
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        response = model.generate_content(
            [prompt, {"mime_type": "application/pdf", "data": pdf_bytes}]
        )

        # --- Clean up ---
        os.remove(pdf_path)

        return jsonify({
            "prompt": prompt,
            "answer": response.text.strip() if response.text else "(No text response returned)"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(debug=True)
