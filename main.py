from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/generate-voice', methods=['POST'])
def generate_voice():
    # Extract parameters from JSON body
    language = request.json.get('front_tryme_language')
    voice = request.json.get('front_tryme_voice')
    text = request.json.get('front_tryme_text')

    if not all([language, voice, text]):
        return jsonify({'error': 'Missing one or more required fields: front_tryme_language, front_tryme_voice, front_tryme_text'}), 400

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://aivoicegenerator.com',
        'Referer': 'https://aivoicegenerator.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Cookie': 'csrf_cookie_name=30532c02cafbab8dfe5a24e3d230c472; ci_session=dtdd9mn0e3vh3pp6m2u3qvkeevmsa420; site_lang=english',
    }

    data = {
        'csrf_test_name': '30532c02cafbab8dfe5a24e3d230c472',
        'front_tryme_language': language,
        'front_tryme_voice': voice,
        'front_tryme_text': text,
    }

    response = requests.post('https://aivoicegenerator.com/home/tryme_action/', headers=headers, data=data)

    try:
        return jsonify(response.json())
    except ValueError:
        return jsonify({'error': 'Invalid JSON returned from API'}), 500

if __name__ == '__main__':
    app.run(debug=True)