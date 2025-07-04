# Business Card Extractor

A modern web app to extract structured data from business card images using Groq's LLM and optionally save the results to Google Sheets or download as CSV.  
Built with Flask, ready for deployment on [Render](https://render.com/).

---

## Features

- **Upload business card images** (PNG, JPG, JPEG)
- **Extracts:** name, email, phone, websites, organization, designation, address
- **Save to Google Sheets** (just provide a Sheet URL and share with our service account)
- **Or download as CSV** (if no Sheet URL is provided)
- **Modern, responsive UI** with drag-and-drop support

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/business-card-extractor.git
cd business-card-extractor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

You need a Groq API key.  
Create a `.env` file or set the variable in your environment:

```bash
export GROQ_API_KEY=your_groq_api_key_here
```

### 4. Google Sheets Integration

- Go to [Google Cloud Console](https://console.cloud.google.com/).
- Create a Service Account and download the `credentials.json` file.
- Place `credentials.json` in your project root.
- **Share your Google Sheet** with the service account email (e.g. `business-cards@businesscards-464915.iam.gserviceaccount.com`) as an **Editor**.

### 5. Run the app locally

```bash
python app.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## Deploying on Render

1. **Push your code to GitHub.**
2. **Create a new Web Service** on [Render](https://render.com/).
3. **Set build and start commands:**
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
4. **Add environment variables** (e.g. `GROQ_API_KEY`).
5. **Add `credentials.json`** as a secret file or commit it (not recommended for public repos).
6. **Deploy!**

---

## File Structure

```
.
├── app.py
├── requirements.txt
├── Procfile
├── credentials.json
├── templates/
│   └── index.html
├── static/
│   └── (optional static files)
```

---

## Notes

- If you do **not** provide a Google Sheet URL, the app will return a CSV file for download.
- The UI is fully responsive and works on mobile and desktop.
- For Google Sheets, the first row will be bold headers.

---

## License
```
MIT License

Copyright (c) 2025 Aaditya Mehetre

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
---

## Credits

- [Groq](https://groq.com/)
- [Flask](https://flask.palletsprojects.com/)
- [gspread](https://gspread.readthedocs.io/)
- [oauth2client](https://github.com/googleapis/oauth2client) 
