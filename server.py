from flask import Flask, request, jsonify
from smart_summarizer_agent import run_agent

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    page_text = data.get("text", "")
    if not page_text.strip():
        return jsonify({"error": "No text provided"}), 400

    try:
        run_agent(page_text)
        return jsonify({"status": "success", "message": "Note saved successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
