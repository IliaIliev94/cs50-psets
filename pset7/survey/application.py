import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request


# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    # Get the submission data from the form and append it to the csv file. Redirect the user to the sheet route.
    if request.method == 'POST':
        name = request.form.get("name")
        rank = request.form.get("rank")
        role = request.form.get("role")
        if not name or not rank or not role:
            return render_template("error.html", message="400 Invalid form data")
        else:
            with open('survey.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([name, rank, role])
    return redirect('/sheet')


@app.route("/sheet", methods=["GET"])
def get_sheet():
    # Read the survey file and append the submission data to the players list
    with open('survey.csv', 'r', newline="") as f:
        reader = csv.reader(f)
        players = list(reader)
    print(players)
    # Display the sheets html file and pass the players list to it
    return render_template("sheets.html", players=players)
