from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

from models import Patient
from lru import LRUCache
from graph import Graph
from predict import predict_disease, assign_doctor

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        disease TEXT,
        doctor TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

cache = LRUCache(5)

g = Graph(5)
g.addEdge(0,1)
g.addEdge(1,2)
g.addEdge(2,3)
g.addEdge(3,4)

@app.route("/")
def home():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM patients")
    total = cur.fetchone()[0]

    cur.execute("SELECT disease, COUNT(*) FROM patients GROUP BY disease ORDER BY COUNT(*) DESC LIMIT 1")
    common = cur.fetchone()

    conn.close()

    return render_template("home.html", total=total, common=common)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        symptoms = request.form.getlist("symptoms")

        disease = predict_disease(symptoms)
        doctor = assign_doctor(disease)
        date = datetime.now().strftime("%Y-%m-%d")

        patient = Patient(name, age, disease)

        conn = get_db()
        conn.execute(
            "INSERT INTO patients(name,age,disease,doctor,date) VALUES (?,?,?,?,?)",
            (name, age, disease, doctor, date)
        )
        conn.commit()
        conn.close()

        cache.put(name, patient.get_info())

        return redirect("/patients")

    return render_template("register.html")

@app.route("/patients")
def patients():
    search = request.args.get("search")

    conn = get_db()
    cur = conn.cursor()

    if search:
        cur.execute("SELECT * FROM patients WHERE name LIKE ?", ('%'+search+'%',))
    else:
        cur.execute("SELECT * FROM patients")

    data = cur.fetchall()
    conn.close()

    return render_template("patients.html", data=data)

@app.route("/cache")
def cache_view():
    return {"recent": cache.get_cache()}

@app.route("/graph")
def graph_view():
    return {"BFS": g.BFS(0), "DFS": g.DFS(0)}

if __name__ == "__main__":
    app.run(debug=True)