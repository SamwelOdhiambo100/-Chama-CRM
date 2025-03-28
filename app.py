from flask import Flask, render_template, request, flash, redirect, url_for
import json
import os
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "secret_key"  # Required for flash messages

data_file = "chama_data.json"

def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            return json.load(f)
    else:
        return {"members": {}, "contributions": []}

def save_data(data):
    with open(data_file, "w") as f:
        json.dump(data, f, indent=4)

def calculate_progress(member_balance, current_date):
    start_date = date(current_date.year, 1, 1)
    days = (current_date - start_date).days + 1
    expected_amount = days * 20

    progress = (member_balance / expected_amount) * 100 if expected_amount else 0
    return progress, expected_amount

def get_financial_status(progress):
    if progress >= 110:
        return "Excellent", "green"  # Exceeding expectations
    elif progress >= 90:
        return "Good", "lightgreen"  # On track
    elif progress >= 70:
        return "Fair", "yellow"  # Some catching up needed
    else:
        return "Critical", "red"  # Significant shortfall

@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()
    members = data["members"]
    contributions = data["contributions"]

    current_date = date.today()
    member_statuses = {}
    for name, balance in members.items():
        progress, expected = calculate_progress(balance, current_date)
        status, color = get_financial_status(progress)
        member_statuses[name] = {"progress": progress, "status": status, "color": color, "expected": expected, "balance": balance}

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add_member":
            name = request.form.get("member_name")
            if name and name not in members:
                members[name] = 0
                save_data(data)
                flash(f"🎉 {name} added successfully!", "success")
            elif not name:
                flash("⚠️ Member name cannot be empty.", "error")
            else:
                flash(f"🤔 {name} is already a member.", "error")

        elif action == "record_contribution":
            name = request.form.get("contribution_name")
            amount = request.form.get("amount")
            date_str = request.form.get("date")

            if name and amount and date_str:
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date() # convert string to date object
                    amount = float(amount)
                    if name in members:
                        members[name] += amount
                        contributions.append({"member": name, "amount": amount, "date": date_str})
                        save_data(data)
                        flash(f"💰 {name} contributed {amount}. New balance: {members[name]}", "success")
                    else:
                        flash(f"🚫 {name} is not a member.", "error")
                except ValueError:
                    flash("📅 Invalid date or amount format.", "error")
            else:
                flash("📝 Please fill in all contribution fields.", "error")
        elif action == "view_balance":
            name = request.form.get("balance_name")
            if name and name in members:
                flash(f"💵 {name}'s balance: {members[name]}", "success")
            elif not name:
                flash("👤 Please enter a member name", "error")
            else:
                flash(f"❌ {name} is not a member.", "error")

    return render_template("index.html", members=members, contributions=contributions, member_statuses=member_statuses)

@app.route("/clear_data", methods=["POST"])
def clear_data():
    empty_data = {"members": {}, "contributions": []}
    save_data(empty_data)
    flash("Data cleared successfully!", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

