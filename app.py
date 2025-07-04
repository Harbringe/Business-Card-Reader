# app.py

import os
import base64
import json
import csv
import re
from flask import Flask, request, render_template, redirect, url_for, send_file, make_response
from werkzeug.utils import secure_filename
from groq import Groq
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import io

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load Groq
key = os.environ.get("GROQ_API_KEY")
if not key:
    raise RuntimeError("GROQ_API_KEY environment variable is not set. Please set it before running the app.")
client = Groq(api_key=key)

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Google Sheets Setup
def init_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    return gspread.authorize(creds)

def extract_top_level_json(text):
    brace_stack = []
    start = None

    for i, char in enumerate(text):
        if char == '{':
            if start is None:
                start = i  
            brace_stack.append('{')
        elif char == '}':
            if brace_stack:
                brace_stack.pop()
                if not brace_stack:
                    
                    json_candidate = text[start:i + 1]
                    try:
                        return json.loads(json_candidate)
                    except json.JSONDecodeError:
                        start = None  
    return {}  


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        sheet_url = request.form.get("sheet_url")

        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            with open(filepath, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            image_data_url = f"data:image/jpeg;base64,{encoded_image}"

            # Groq API call
            completion = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": [
                {
                    "type": "text",
                    "text": "Extract all the visible text from this business card image. Do not explain anything, just output the text. The output format must follow a specific json: {\"name\": _, \"email\": _ , \"phone:\" _, \"list_of_websites\" (complete link if only icon is used and handle is given): [], \"organization\" : _, \"designation\": _, \"address\": _ }"
                },
                            {
                                "type": "image_url",
                                "image_url": { "url": image_data_url }
                            }
                        ]
                    }
                ],
                temperature=0.5,
                max_completion_tokens=1024,
                top_p=1,
                stream=False
            )

            result = completion.choices[0].message.content
            print(result)

            data = extract_top_level_json(result)
            if not data:
                return "❌ Error: Could not extract valid JSON from the Groq API response."
            
            print("\n \n ")
            print(json.dumps(data, indent=4))
            print("\n \n ")

            # Prepare row for both Google Sheets and CSV
            headers = ["name", "email", "phone", "list_of_websites", "organization", "designation", "address"]
            row = [
                data.get("name", ""),
                data.get("email", ""),
                data.get("phone", ""),
                ", ".join(data.get("list_of_websites", [])),
                data.get("organization", ""),
                data.get("designation", ""),
                data.get("address", "")
            ]

            # Append to Google Sheet
            if sheet_url:
                gc = init_google_sheets()
                sheet = gc.open_by_url(sheet_url).sheet1
                # Check if the sheet is empty (no data)
                existing = sheet.get_all_values()
                if not existing:
                    sheet.append_row(headers)
                    # Make header bold
                    fmt = {'textFormat': {'bold': True}}
                    sheet.format('1:1', fmt)
                elif existing and existing[0] != headers:
                    sheet.delete_rows(1)
                    sheet.insert_row(headers, 1)
                    sheet.format('1:1', {'textFormat': {'bold': True}})
                sheet.append_row(row)
                return "✅ Data added to Google Sheet!"
            
            # Else, return CSV as download
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(headers)
            writer.writerow(row)
            output.seek(0)
            response = make_response(output.getvalue())
            response.headers["Content-Disposition"] = "attachment; filename=business_card.csv"
            response.headers["Content-type"] = "text/csv"
            return response

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)