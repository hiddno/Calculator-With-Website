from flask import Flask, render_template, request
import json
import os
import math

app = Flask(__name__)

HISTORY_FILE = "history.json"
MAX_HISTORY = 50


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-MAX_HISTORY:], f)


def calculate(expr):
    expr = expr.replace("×", "*").replace("÷", "/")
    return eval(expr)


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    expression = ""
    history = load_history()

    if request.method == "POST":
        expression = request.form.get("expression", "")

        if request.form.get("action") == "clear_history":
            save_history([])
            history = []

        else:
            try:
                result = calculate(expression)
                history.append(f"{expression} = {result}")
                save_history(history)
            except:
                result = "Error"

    return render_template(
        "index.html",
        result=result,
        history=reversed(history),
        expression=expression
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)