# Ripasso Uni

A daily **spaced-review** web app for exam prep. Each weekday (Sun–Fri) unlocks a lesson; you take
notes per lesson, browse history, and your progress is saved in the browser.

Two content tracks: **AI / ML** (LLM fundamentals, RAG types, agents, embeddings & retrieval, chatbot
architecture) and **Product Management**.

**Live → https://javas-cri-pt.github.io/ripasso-uni/**

Static build: `curriculum.yml` + `lessons/` → `build-app.py` renders `index.html`. Theme toggle,
mobile drawer, inline SVG system-design diagrams. No backend, no accounts — everything runs client-side.
