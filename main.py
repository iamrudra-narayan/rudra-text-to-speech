import json
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import requests
import os

load_dotenv()  # Loads from .env file

app = FastAPI(title="FreeTTS Voice Generator API", version="1.0")

AUTH_KEY = os.getenv("AUTHORIZATION_KEY")

class TTSRequest(BaseModel):
    text: str
    type: int
    ssml: int
    voiceType: str
    languageCode: str
    voiceName: str
    gender: str
    speed: str
    pitch: str
    volume: str
    format: str
    quality: int
    isListenlingMode: int
    displayName: str


class TTSResponse(BaseModel):
    code: int
    message: str
    audiourl: Optional[str] = None

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rudra Text-to-Speech API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding-top: 50px;
                background-color: #f4f4f4;
            }
            a {
                display: inline-block;
                margin-top: 20px;
                font-size: 20px;
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 6px;
            }
            a:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to Rudra Text-to-Speech API</h1>
        <p>Click below to explore the API documentation.</p>
        <a href="/docs" target="_blank">View API Docs</a>
    </body>
    </html>
    """

@app.post("/generate-freetts", response_model=TTSResponse)
def generate_freetts(request_body: List[TTSRequest]):
    url = "https://freetts.com/text-to-speech"

    headers = {
        "accept": "text/x-component",
        "accept-language": "en-US,en;q=0.7",
        "content-type": "text/plain;charset=UTF-8",
        "next-action": "f6a37f3b9ffdb01ba2da16f264fdabab4a254f61",
        "next-router-state-tree": "%5B%22%22%2C%7B%22children%22%3A%5B%22(functions)%22%2C%7B%22children%22%3A%5B%22text-to-speech%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Ftext-to-speech%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D",
        "origin": "https://freetts.com",
        "priority": "u=1, i",
        "referer": "https://freetts.com/text-to-speech",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Cookie": f"Authorization={AUTH_KEY}"
    }

    try:
        payload = [item.dict() for item in request_body]
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        # Response is not valid JSON — it's a multi-line text stream
        lines = response.text.splitlines()

        # Find the line that starts with `1:` and get the JSON part
        for line in lines:
            if line.startswith("1:"):
                json_part = line[2:]  # Remove the `1:` prefix
                parsed = json.loads(json_part)
                audiourl = parsed.get("data", {}).get("audiourl")
                code = parsed.get("code", 500)

                if audiourl:
                    return TTSResponse(
                        code=code,
                        message="Voice generated successfully.",
                        audiourl=audiourl
                    )

        raise HTTPException(status_code=400, detail="Valid audio URL not found in response")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"FreeTTS request failed: {str(e)}")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=502, detail=f"FreeTTS returned invalid JSON format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")