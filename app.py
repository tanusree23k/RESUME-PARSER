from flask import Flask, render_template, request
import PyPDF2
import re

app = Flask(__name__)

def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        file = request.files["resume"]

        if file:
            text = extract_text(file)

            email = re.findall(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                text
            )

            phone = re.findall(
                r"\d{10}",
                text
            )

            skills = []

            skill_list = [
                "Python", "Java", "SQL",
                "HTML", "CSS", "JavaScript",
                "Machine Learning"
            ]

            for skill in skill_list:
                if skill.lower() in text.lower():
                    skills.append(skill)

            result = {
                "email": email[0] if email else "Not Found",
                "phone": phone[0] if phone else "Not Found",
                "skills": skills
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)