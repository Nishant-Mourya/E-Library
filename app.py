import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database config
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///books.db")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ---------------- Models ----------------
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_link = db.Column(db.String(250), nullable=True)

# ---------------- Routes ----------------
@app.route("/")
def home():
    if "role" in session:
        if session["role"] == "admin":
            return redirect(url_for("admin_dashboard"))
        else:
            return redirect(url_for("books"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["role"] = "admin"
            flash("Welcome Admin!", "success")
            return redirect(url_for("admin_dashboard"))
        elif username == "reader" and password == "reader123":
            session["role"] = "reader"
            flash("Welcome Reader!", "success")
            return redirect(url_for("books"))
        else:
            flash("Invalid credentials", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have logged out.", "info")
    return redirect(url_for("login"))

# ---------------- Reader View ----------------
@app.route("/books")
def books():
    if "role" not in session:
        return redirect(url_for("login"))
    all_books = Book.query.all()
    return render_template("books.html", books=all_books)

# ---------------- Admin View ----------------
@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("login"))
    books = Book.query.all()
    return render_template("admin_dashboard.html", books=books)

@app.route("/admin/add", methods=["POST"])
def add_book():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    title = request.form["title"]
    author = request.form["author"]
    category = request.form["category"]
    description = request.form["description"]
    file_link = request.form["file_link"]

    new_book = Book(title=title, author=author, category=category, description=description, file_link=file_link)
    db.session.add(new_book)
    db.session.commit()
    flash("Book added successfully!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/edit/<int:id>", methods=["POST"])
def edit_book(id):
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    book = Book.query.get_or_404(id)
    book.title = request.form["title"]
    book.author = request.form["author"]
    book.category = request.form["category"]
    book.description = request.form["description"]
    book.file_link = request.form["file_link"]
    db.session.commit()
    flash("Book updated successfully!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete/<int:id>", methods=["POST"])
def delete_book(id):
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted!", "danger")
    return redirect(url_for("admin_dashboard"))

# ---------------- Run ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
