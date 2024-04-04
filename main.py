from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
import os

PASSWORD = os.getenv("job_application")

app = Flask(__name__)
app.config["SECRET_KEY"] = "Dhruva@1"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "workdhruvateja@gmail.com"
app.config["MAIL_PASSWORD"] = PASSWORD
db = SQLAlchemy(app)

mail = Mail(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(255))

@app.route("/", methods=["GET", "POST"])

def home():
    if request.method == "POST":
        first_name = request.form["fname"]
        last_name = request.form["lname"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]
        print(first_name, last_name, email, date, occupation)
        
        form_vr = Form(first_name=first_name, last_name=last_name, email=email, date=date_obj, occupation=occupation)
        db.session.add(form_vr)
        db.session.commit()

        message_body = f"""
                    Thank you for your submission, {first_name}
                    Here are your data:
                    {first_name} {last_name}
                    {date}
                    {occupation}
                    Thank you!
                    """
        message = Message(subject="New Form Submission",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body = message_body)
        flash(f"{first_name}, your form submitted Successfully!", "success")

        mail.send(message)

    return render_template("index.html")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)