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


def send_email_via_resend(to, subject, html):
    api_key = os.environ.get("RESEND_API_KEY")
    url = "https://api.resend.com/emails"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "from": "Your Website <onboarding@resend.dev>",
        "to": [to],
        "subject": subject,
        "html": html
    }

    response = requests.post(url, headers=headers, json=data)
    print("Email response:", response.status_code, response.text)
    return response.status_code == 200

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
        send_email_via_resend(
            to=os.environ.get("TARGET_EMAIL"),
            subject=f"New contact form submission from {name}",
            html=f"""
                <h2>New message received!</h2>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Message:</strong><br>{message}</p>
            """
        )
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
