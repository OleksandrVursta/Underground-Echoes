# Underground Echoes 🤘

**Elevator Pitch:** ШІ-агент для пошуку справжнього музичного андеграунду. Бот допомагає меломанам вийти за межі "бульбашки" мейнстрімних алгоритмів Spotify, знаходячи реальні нішеві гурти зі схожим звучанням.

## 🎯 Цільова аудиторія
Меломани, фанати важкої сцени (Metal, Punk, Hardcore) та студенти-розробники, які цікавляться інтеграцією LLM з реальними API.

## 🛠 Технології та Патерни
- **LLM:** `OpenAI o3-mini` — обрано за здатність до складних міркувань (reasoning), що дозволяє ефективно розрізняти "культовий андеграунд" та "локальні проекти".
- **External API:** `Spotify Web API (Spotipy)` — для верифікації існування гуртів та отримання прямих посилань на профілі.
- **Validation:** Гібридна система перевірки. Використовується `SequenceMatcher` для відсікання помилкових результатів пошуку (коли Spotify підсовує мейнстрім замість нішевого гурту з подібною назвою).
- **UI:** Telegram Bot (`pyTelegramBotAPI`).

## 📁 Структура проекту
- `bot.py` — точка входу, обробка Telegram-подій.
- `services/` — логіка взаємодії з OpenAI та Spotify.
- `utils/` — валідатори вводу та допоміжні функції.
- `handlers/` — модульна обробка команд.

## 🚀 Як запустити
1. **Клонуйте репозиторій:**
   ```bash
   git clone https://github.com/OleksandrVursta/Underground-Echoes.git
   cd underground-echoes
2. **Встановіть залежності:**
   ```bash
   pip install -r requirements.txt
3. **Налаштуйте середовище:**
   Створіть файл `.env` у кореневій папці (використовуйте `.env.example` як шаблон) та додайте ваші ключі:

   - 🔑 `TELEGRAM_TOKEN` — отримати у [@BotFather](https://t.me/BotFather)
   - 🧠 `OPENAI_API_KEY` — отримати на [platform.openai.com](https://platform.openai.com/)
   - 🎸 `SPOTIPY_CLIENT_ID` — отримати в [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - 🔐 `SPOTIPY_CLIENT_SECRET` — ваш секретний ключ Spotify
4. **Запустіть бота:**
   ```bash
   python bot.py

## 📝 Нотатки по реалізації
- **Бот використовує стратегію "Over-fetching":**.
- 📡 Запитує у ШІ 15-20 варіантів гуртів.
- 🔍 Фільтрує їх через Spotify API на відповідність назви та наявність реальних треків.
- 💎 Видає користувачу "чисту" п'ятірку найкращих результатів без "галюцинацій" та порожніх посилань.


### 🏗 Архітектура системи

```mermaid
graph TD
    %% Користувач та інтерфейс
    User((Користувач 🤘)) <-->|Назва гурту| Bot[bot.py: Telegram Bot]

    subgraph Backend [Серверна логіка]
        Bot -->|1. Валідація| Val[utils/validators.py]
        Bot -->|2. Статус| Status[bot.reply_to: ⏳ Занурююсь...]
    end

    subgraph AI_Layer [Інтелектуальний рівень]
        Bot -->|3. Over-fetching запит| OpenAI[services/openai_service.py: o3-mini]
        OpenAI -->|4. Список: 20 кандидатів| Bot
    end

    subgraph Search_Layer [Верифікація Spotify]
        Bot -->|5. Фільтрація| Spot[services/spotify_service.py: Spotipy]
        Spot <-->|6. Пошук & SequenceMatcher| SpAPI[Spotify Web API]
        Spot -->|7. Топ-5 перевірених| Bot
    end

    %% Фінал
    Bot -->|8. Видалення статусу| Del[bot.delete_message]
    Bot -->|9. Результат| User

    %% Стилі
    style User fill:#000,color:#fff,stroke:#333
    style Bot fill:#24A1DE,color:#fff,stroke:#333,stroke-width:2px
    style OpenAI fill:#74aa9c,color:#fff,stroke:#000
    style Spot fill:#1DB954,color:#000,stroke:#000
    style Status fill:#f9f,stroke-dasharray: 5 5