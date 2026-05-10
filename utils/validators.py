def validate_music_request(text: str):
    if not text or len(text.strip()) == 0:
        return False, "Повідомлення не може бути порожнім. Напиши назву гурту!"

    if len(text) > 100:
        return False, "Назва занадто довга. Будь ласка, вкажи лише назву гурту або виконавця."

    forbidden_keywords = ["ignore", "ігноруй", "system prompt", "ти — не"]
    if any(word in text.lower() for word in forbidden_keywords):
        return False, "Гарна спроба, але я працюю тільки з музикою! 😉"
    
    return True, None