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

graph TD
    %% Nodes
    User((Користувач 🤘))
    Bot[bot.py: Telegram Bot]
    Validators[utils/validators.py]
    Processing[bot.reply_to: Статус]
    OpenAI[services/openai_service.py: o3-mini]
    Spotify[services/spotify_service.py: Spotipy]
    SpAPI[Spotify Web API]
    Del[bot.delete_message]

    %% Flow
    User <-->|Повідомлення| Bot
    
    subgraph Logic [Ядро логіки]
        Bot --> Validators
        Bot --> Processing
    end

    subgraph AI [Інтелектуальний рівень]
        Bot -->|Over-fetching| OpenAI
        OpenAI -->|JSON: 20 варіантів| Bot
    end

    subgraph Search [Верифікація Spotify]
        Bot --> Spotify
        Spotify <-->|SequenceMatcher| SpAPI
        Spotify -->|Топ-5 валідних| Bot
    end

    Bot --> Del
    Bot -->|Результат| User

    %% Styling
    style User fill:#000,color:#fff,stroke:#333
    style Bot fill:#24A1DE,color:#fff,stroke:#333,stroke-width:2px
    style OpenAI fill:#74aa9c,color:#fff,stroke:#000
    style Spotify fill:#1DB954,color:#000,stroke:#000
    style Processing fill:#f9f,stroke-dasharray: 5 5