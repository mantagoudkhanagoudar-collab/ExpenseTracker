from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

FILE_NAME = "expenses.json"

def load_expenses():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(FILE_NAME, "w") as f:
        json.dump(expenses, f, indent=4)

@app.route("/")
def index():
    expenses = load_expenses()
    total = sum(exp["amount"] for exp in expenses)

    # Create category-wise totals
    category_data = {}
    for exp in expenses:
        cat = exp["category"]
        category_data[cat] = category_data.get(cat, 0) + exp["amount"]

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        categories=list(category_data.keys()),   
        amounts=list(category_data.values())     
    )

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        category = request.form["category"]
        amount = float(request.form["amount"])
        date = request.form["date"] or datetime.now().strftime("%Y-%m-%d")

        expenses = load_expenses()

        expenses.append({
            "category": category,
            "amount": amount,
            "date": date
        })

        save_expenses(expenses)
        return redirect("/")

    return render_template("add.html")

@app.route("/delete/<int:index>")
def delete(index):
    expenses = load_expenses()
    
    if 0 <= index < len(expenses):
        expenses.pop(index)
        save_expenses(expenses)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)