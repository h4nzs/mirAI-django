# mirAI-django 🎬🤖

**mirAI-django** is an AI-powered movie recommendation web app built with Django. Created originally as a university project, this platform leverages Google Gemini (Generative AI) and The Movie Database (TMDB) API to help users discover the perfect movie through engaging, conversational recommendations. Designed for movie enthusiasts, students, and anyone who loves exploring new films, mirAI-django offers a modern, intuitive UX styled with Tailwind CSS and daisyUI.

---

## 🚀 Features

- **Conversational Movie Recommendations**: Interact with an AI chatbot that guides your movie discovery with smart, friendly questions and suggestions.
- **TMDB Integration**: Explore trending, popular, top-rated, now-playing, and upcoming movies from the TMDB API.
- **Personalized Suggestions**: The AI gathers info about your tastes mid-conversation (genre, actors, mood, etc.) and responds with concise JSON-powered recommendations.
- **User Dashboard**: Save favorite movies, browse details, and organize watchlists.
- **Modern UI**: Powered by Django, Tailwind CSS v4, and daisyUI for a responsive and visually appealing interface.
- **Classic Registration**: Secure, straightforward sign-up and account management (no social login required).

---

## 💻 Tech Stack

- **Backend**: Django 5, PostgreSQL
- **Frontend**: Tailwind CSS, daisyUI, PostCSS
- **AI**: Google Generative AI (Gemini)
- **Movie Data**: TMDB API

---

## 🏗️ Project Structure

```plaintext
mirAI-django/
│
├── mirAI/                 # Project config & main settings
├── mirai/                 # Tailwind & theme app (CSS pipeline)
├── core/                  # Authentication, core URLs
├── dashboard/             # User dashboard features
├── movies/                # Movies (lists, search, details)
├── ai/                    # Conversational AI endpoints
├── services/              # Integrations: ai_google.py, tmdb.py
├── static/                # Production CSS & static files
├── static_src/            # Tailwind CSS (+ PostCSS) source
├── templates/             # HTML templates
└── .env                   # API keys, secrets
```

---

## 🛠️ Quickstart

### 1. Clone and Setup

```sh
git clone https://github.com/h4nzs/mirAI-django.git
cd mirAI-django
```

### 2. Environment Variables

Create a `.env` file in the root with variables such as:

- `DJANGO_SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `TMDB_API_KEY`
- `GOOGLE_AI_API_KEY`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

### 3. Install Dependencies

**Python:**
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Node (for Tailwind CSS pipeline):**
```sh
cd mirai/static_src
npm install
npm run build
```

### 4. Database & Run

```sh
python manage.py migrate
python manage.py runserver
```
Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 📣 Contributing

Pull requests and issues are welcome—especially from fellow movie lovers and students interested in AI or Django!

---

## 📄 License

MIT License © [h4nzs](https://github.com/h4nzs)

---

## 📝 About

This project was created as part of a university assignment, so if you’re learning Django, exploring AI movie chatbots, or just passionate about film, you’re the perfect user!

---
