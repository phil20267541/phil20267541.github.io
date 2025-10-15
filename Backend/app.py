from unicodedata import name
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SUPABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({"message": "Backend is running!"})

@app.route('/api/index/data')
def get_data():
    cv_description = (
        "As my first fully fledged website, I have used the creation of my CV website "
        "as a learning experience to test my knowledge of HTML and CSS. From this I "
        "have been able to learn responsive styling and key principles of website development. "
        "Visit my CV now to see what I can do for you."
    )

    content = [
        {
            "title": "CV",
            "description": cv_description,
            "link": "https://phil20267541.github.io/CV_Website/",
            "image": "Resources/cv.png"
        },
        {
            "title": "Shoop",
            "description": "All hail the shoop",
            "link": "https://phil20267541.github.io/Shoop/",
            "image": "Resources/shoop.png"
        }
    ]

    projects = [
        {"title": "CV", "link": "#cv"},
        {"title": "Shoop", "link": "#shoop"}
    ]

    # Return both in a single JSON object
    return jsonify({
        "content": content,
        "projects": projects,
        "success": True
    })
    
@app.route('/api/contact/submit', methods=['POST'])
def submit_contact():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
       
    errors = {}
    if not name:
        errors['name'] = "Name is required."
    if not email:
        errors['email'] = "Email is required."
    if not message:
        errors['message'] = "Message is required."
    
    if errors:
        return jsonify({"errors": errors}), 400
    else:
        new_entry = Submission(name=name, email=email, message=message)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"success": True, "message": "Form submitted successfully!"}), 200

if __name__ == '__main__':
    app.run()
