from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Backend is running!"})

@app.route('/api/data')
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
        "projects": projects
    })

if __name__ == '__main__':
    app.run()
