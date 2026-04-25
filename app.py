from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create DB and table
def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (amount REAL, category TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]

        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("INSERT INTO expenses VALUES (?, ?)", (amount, category))
        conn.commit()
        conn.close()

    # Fetch summary
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = c.fetchall()
    conn.close()

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)