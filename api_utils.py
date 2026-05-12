import requests

def translate_text(text, pair="ru|en"):
    try:
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair={pair}"
        response = requests.get(url, timeout=5)
        if response.ok:
            return response.json().get('responseData', {}).get('translatedText', "")
    except Exception:
        return ""
    return ""