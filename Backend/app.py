from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

print("ALL ENV VARIABLES:")
for k, v in os.environ.items():
    print(k, "=", v)

# Read database URL from environment
database_url = os.environ.get("SUPABASE_URL")
if not database_url:
    # Fail fast if missing
    raise RuntimeError("SUPABASE_URL environment variable not set!")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Models
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Optional: Initialize tables via a route instead of at import
@app.route("/initdb")
def init_db():
    try:
        db.create_all()
        return {"success": True, "message": "Tables created!"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Routes
@app.route("/")
def home():
    return jsonify({"message": "Backend is running!"})

@app.route("/dbtest")
def db_test():
    try:
        with db.engine.connect() as conn:
            conn.execute("SELECT 1")
        return jsonify({"success": True, "message": "Connected successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

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

if __name__ == "__main__":
    app.run()
