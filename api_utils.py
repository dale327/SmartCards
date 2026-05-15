import re

import translators as ts


def translate_text(text):
    if not text or len(text.strip()) == 0:
        return ""

    is_russian = bool(re.search('[а-яА-Я]', text))
    from_lang = 'ru' if is_russian else 'en'
    to_lang = 'en' if is_russian else 'ru'

    engines = ['yandex', 'bing', 'google']

    for engine in engines:
        try:
            result = ts.translate_text(
                query_text=text,
                translator=engine,
                from_language=from_lang,
                to_language=to_lang,
                timeout=5
            )
            if result:
                return result
        except Exception as e:
            print(f"Сервис {engine} временно недоступен: {e}")
            continue

    return "Ошибка перевода"
