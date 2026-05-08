import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from services.spotify_service import get_artist_stats

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_recommendations(band_name):
    system_prompt = (
        f"Ти — експерт з музичного андеграунду. Знайди 15 РЕАЛЬНИХ гуртів, схожих на '{band_name}'.\n\n"
        "СУВОРІ КРИТЕРІЇ:\n"
        "1. НІШЕВІСТЬ: Обирай гурти, які мають статус культових або маловідомих. Уникай зірок першої величини.\n"
        "2. ЖАНРИ: Пиши назви жанрів як цілі слова, через кому (наприклад: 'Heavy Metal, Epic Metal').\n"
        "3. МОВА: Назви гуртів — англійською, все інше — українською.\n"
        "4. ФОРМАТ: Поверни JSON об'єкт: "
        "{\"bands\": [{\"name\": \"Name\", \"reason\": \"чому схожий\", \"genres\": \"жанр1, жанр2\"}]}"
    )

    try:
        response = client.chat.completions.create(
            model="o3-mini", 
            messages=[{"role": "user", "content": system_prompt}],
            response_format={ "type": "json_object" }
        )
        
        data = json.loads(response.choices[0].message.content)
        suggested_data = data.get("bands", [])
        
        final_results = []
        for band in suggested_data:
            if len(final_results) >= 5:
                break
                
            name = band['name']
            stats = get_artist_stats(name)
            
            if not stats or not stats.get('url'):
                continue

            genres = band.get('genres', 'Underground')
            if isinstance(genres, list):
                genres = ", ".join(genres)

            final_results.append(
                f"🎸 **{name}**\n"
                f"🏷 Жанри: {genres}\n"
                f"🤔 {band.get('reason')}\n"
                f"🔗 [Слухати в Spotify]({stats['url']})"
            )

        return "\n\n".join(final_results) if final_results else "❌ Нічого не знайдено."

    except Exception as e:
        print(f"ERROR: {e}")
        return "⚠️ Помилка підбору рекомендацій."