from unicodedata import name
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import requests
import resend


app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
resend.api_key = os.environ.get("RESEND_API_KEY")

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
    
    # Prepare REST API request to Supabase
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    payload = {
        "name": name,
        "email": email,
        "message": message
    }

    response = requests.post(f"{SUPABASE_URL}/rest/v1/submissions", json=payload, headers=headers)

    try:
        # Send to yourself
        resend.Emails.send({
            "from": "Phil2026741's Projects <onboarding@resend.dev>",
            "to": os.environ.get("TARGET_EMAIL"),
            "subject": f"New message from {name}",
            "html": f"""
                <div style="background-color: #7B2CBF;padding: 10px;margin: 0;">
                    <h2 style="font-size: 40px;justify-self: center;color: #F0F4FF;padding: 0;margin: 0;">New Contact Form Submission</h2>
                </div>
                <div style="background-color: #F0F4FF;padding: 20px;margin: 0;">
                    <p style="font-size: 25px;color: #1A1A2E;padding: 0;margin: 0;"><strong>Name:</strong> {name}</p>
                    <p style="font-size: 25px;color: #1A1A2E;padding: 0;margin: 0;"><strong>Email:</strong> {email}</p>
                    <p style="font-size: 25px;color: #1A1A2E;padding: 0;margin: 0;"><strong>Message:</strong><br>{message}</p>
                </div>
            """
        })
    except Exception as e:
        print("Email error:", e)
    
    if response.status_code in (200, 201):
        return jsonify({"success": True, "message": "Form submitted successfully!"})
    else:
        return jsonify({
            "success": False,
            "error": response.text
        }), response.status_code


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
