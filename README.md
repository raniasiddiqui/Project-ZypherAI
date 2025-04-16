## 🧠 Async Prediction API with Flask + Redis Queue
This project implements a Flask-based machine learning prediction API with both synchronous and asynchronous support. Asynchronous predictions are processed using a custom queue built with Redis and a background worker thread.

## 📦 Features
- ✅ Sync & Async prediction via /predict endpoint

- ⚙️ Redis-powered queue for async tasks

- 🔄 Background thread to consume and process tasks

- 🧾 Result retrieval via /predict/<prediction_id> endpoint

- 🐳 Docker + Docker Compose ready

