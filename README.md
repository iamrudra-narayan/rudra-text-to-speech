# 🔡 AI Text To Speech API

A FastAPI-based application that generates human-like speech using FreeTTS. Easily deployable on [Render.com](https://render.com), and perfect for projects needing text-to-speech functionality.

---

##

## 🔧 Installation & Setup

### ✅ Install dependencies:

```bash
pip install "fastapi[standard]"
pip install requests
pip install python-dotenv
pip install gunicorn
```

### ✅ Create `.env` file:

```env
AUTHORIZATION_KEY=your_freetts_cookie_token
```

---

##

## 📂 Project Structure

```
├── main.py             # Main FastAPI application
├── .env                # Stores your FreeTTS Authorization token
├── requirements.txt    # Python dependencies
├── Procfile            # Required by Render
├── render.yaml         # Render deployment config
└── README.md           # This documentation
```

---

##

## 🚀 Deploying on Render.com

### 📄 `render.yaml`:

```yaml
services:
  - type: web
    name: fastapi-app
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port 10000
    envVars:
      - key: PORT
        value: 10000
```

### 📄 `Procfile`:

```procfile
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 📄 `requirements.txt`:

```txt
fastapi[standard]
requests
python-dotenv
gunicorn
```

---

##

## 📤 GitHub Push Commands

```bash
git init
git remote add origin https://github.com/yourusername/ai-text-to-speech.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

---

##

## 📦 Example JSON Payload

```json
[
    {
        "text": "Transform this into a classic noir scene — high-contrast black and white, sharp shadows, foggy ambiance, and vintage film grain for my YouTube channel logo",
        "type": 1,
        "ssml": 0,
        "voiceType": "Standard",
        "languageCode": "en-US",
        "voiceName": "Matthew",
        "gender": "Male",
        "speed": "1.0",
        "pitch": "0",
        "volume": "0",
        "format": "mp3",
        "quality": 0,
        "isListenlingMode": 0,
        "displayName": "Matthew Ibarra"
    }
]
```

---

##

## 🧪 CURL Example

```bash
curl -X 'POST' \
  'https://rudra-text-to-speech.onrender.com/generate-freetts' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
    {
        "text": "Transform this into a classic noir scene — high-contrast black and white, sharp shadows, foggy ambiance, and vintage film grain for my YouTube channel logo",
        "type": 1,
        "ssml": 0,
        "voiceType": "Standard",
        "languageCode": "en-US",
        "voiceName": "Matthew",
        "gender": "Male",
        "speed": "1.0",
        "pitch": "0",
        "volume": "0",
        "format": "mp3",
        "quality": 0,
        "isListenlingMode": 0,
        "displayName": "Matthew Ibarra"
    }
]'
```

---

##

## 📁 API Documentation

### 🌐 `GET /`

* **Response**: HTML Welcome Page with link to `/docs`.

---

### 🔊 `POST /generate-freetts`

* **Request**: JSON array of `TTSRequest` items.
* **Response**: Returns a downloadable `audiourl`.

#### ✅ Success Response:

```json
{
  "code": 200,
  "message": "Voice generated successfully.",
  "audiourl": "https://freetts.com/audio/xyz123.mp3"
}
```

#### ❌ Error Responses:

* `400`: Valid audio URL not found.
* `502`: FreeTTS failed or invalid JSON returned.
* `500`: Server-side exception.

---

##

## 🔐 Token Tips

> Get the `Authorization` cookie token from your browser (DevTools > Application > Cookies) while logged in at [FreeTTS](https://freetts.com) and place it in `.env` as:

```env
AUTHORIZATION_KEY=your_cookie_token
```

---

##

## 👨‍💻 Author

**Name**: Rudranarayan Muduli
**API Live**: [https://rudra-text-to-speech.onrender.com](https://rudra-text-to-speech.onrender.com)

---

##

## 📌 Final Notes

* Use responsibly to avoid FreeTTS rate limits.
* Extend by adding a file downloader or UI (Flask/React).
* You can dockerize this app or schedule periodic TTS jobs.
