# CodePal (Minimal Offline Edition)

A tiny Flask web app that helps beginners **generate**, **explain**, and **debug** code for a few languages
without requiring any external API keys. You can optionally wire it to your favorite LLM later.

## Features
- Generate starter snippets for common tasks (calculator, FizzBuzz, to‑do list, guessing game).
- Explain code line‑by‑line in simple language.
- Debug (basic): catches Python syntax errors; performs simple checks for JS/C++/Java.

## Quick Start

```bash
# 1) Create & activate a virtual env (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run the app
python app.py

# 4) Open in your browser
http://127.0.0.1:5000
```

## Optional: Connect to an LLM
This offline edition ships with simple template-based generation. If you want true AI generation,
you can add your own calls inside `services/ai_provider.py` and swap the function used in `app.py`.
(Left as a stub for privacy—no keys required to run.)

## Project Structure
```
codepal/
  app.py
  requirements.txt
  README.md
  templates/
    index.html
  static/
    styles.css
    app.js
```
