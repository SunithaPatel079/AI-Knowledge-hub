from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from database import (
    create_tables,
    add_user,
    get_user,
    add_knowledge,
    get_all_knowledge,
    search_knowledge
)

from ai_service import ask_ai


app = Flask(__name__)

app.secret_key = "knowledge-transfer-secret-key"


create_tables()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            add_user(name, email, password)

            return redirect(url_for("login"))

        except Exception:
            return "Email already registered."

    return render_template("login.html", register=True)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = get_user(email, password)

        if user:

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    return render_template("login.html", register=False)


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    knowledge = get_all_knowledge()

    return render_template(
        "dashboard.html",
        knowledge=knowledge,
        user_name=session["user_name"]
    )


@app.route("/add-knowledge", methods=["GET", "POST"])
def add_knowledge_page():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        title = request.form["title"]
        category = request.form["category"]
        content = request.form["content"]

        add_knowledge(
            title,
            category,
            content,
            session["user_name"]
        )

        return redirect(url_for("dashboard"))

    return render_template("add_knowledge.html")


@app.route("/ask-ai", methods=["GET", "POST"])
def ask_ai_page():

    if "user_id" not in session:
        return redirect(url_for("login"))

    answer = None

    if request.method == "POST":

        question = request.form["question"]

        knowledge = get_all_knowledge()

        knowledge_text = ""

        for item in knowledge:

            knowledge_text += f"""
Title: {item["title"]}
Category: {item["category"]}
Content: {item["content"]}
Author: {item["author"]}

"""

        if knowledge_text:

            answer = ask_ai(
                question,
                knowledge_text
            )

        else:

            answer = (
                "There is no company knowledge available yet."
            )

    return render_template(
        "ask_ai.html",
        answer=answer
    )


@app.route("/search")
def search():

    if "user_id" not in session:
        return redirect(url_for("login"))

    keyword = request.args.get("keyword", "")

    results = search_knowledge(keyword)

    return render_template(
        "dashboard.html",
        knowledge=results,
        user_name=session["user_name"],
        keyword=keyword
    )
if __name__ == "__main__":
    app.run(debug=True)
