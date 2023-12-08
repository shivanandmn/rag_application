from flask import Flask, request, jsonify
from pipeline import QAPipeline

pipe = QAPipeline("config/simple.json")

app = Flask(__name__)


@app.route("/answer", methods=["POST"])
def process_data():
    user_input = request.data.decode("utf-8")
    model_output = pipe.answer(user_input)
    return jsonify({"response": model_output})


if __name__ == "__main__":
    app.run(debug=False)
