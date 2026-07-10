# index.html
🚀 Project Title
ChatTutor

🧠 Problem Statement
Students lack personalized help.

🎯 Objective
AI tutor system.

👥 Target Users
Students

⚙️ Core Features (MVP - achievable in time)
Q&A
Context memory

🌟 Advanced Features (for top teams)
Adaptive learning
🔄 User Flow
Ask → respond

🏗️ System Design Overview
LLM backend

🔌 API Design
POST /ask

🗄️ Database Schema
Conversation

⚠️ Engineering Challenges
Context loss

🧪 Edge Cases
Ambiguous queries

🧰 Suggested Tech Stack
Python

📊 Evaluation Criteria
Innovation
System Design
Code Quality
Completeness
UX

📦 Deliverables (MANDATORY)
Source code

⏱️ Constraints

💡 Bonus Ideas
 📑  History memory


## 📁 Project Tree

```
chat_tutor/
│
├── .env
├── .env.example
├── .gitignore
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── alembic.ini
│
├── logs/
│   ├── app.log
│   └── error.log
│
├── uploads/
│   ├── pdf/
│   ├── images/
│   └── temp/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   └── dashboard.html
│
├── docs/
│   ├── API.md
│   ├── DATABASE.md
│   ├── DEPLOYMENT.md
│   └── ARCHITECTURE.md
│
├── scripts/
│   ├── create_admin.py
│   ├── generate_secret.py
│   ├── seed_database.py
│   ├── backup_database.py
│   └── restore_database.py
│
├── app/
│   │
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── logger.py
│   ├── middleware.py
│   ├── exceptions.py
│   ├── constants.py
│   │
│   ├── auth.py
│   ├── security.py
│   ├── cache.py
│   ├── llm.py
│   │
│   ├── dependencies.py
│   ├── websocket.py
│   │
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── user.py
│   │   ├── session.py
│   │   ├── upload.py
│   │   ├── dashboard.py
│   │   ├── admin.py
│   │   ├── health.py
│   │   └── metrics.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py
│   │   ├── auth_service.py
│   │   ├── cache_service.py
│   │   ├── database_service.py
│   │   ├── pdf_service.py
│   │   ├── image_service.py
│   │   ├── embedding_service.py
│   │   ├── rag_service.py
│   │   ├── prompt_service.py
│   │   ├── email_service.py
│   │   └── analytics_service.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   ├── validators.py
│   │   ├── token_counter.py
│   │   ├── formatter.py
│   │   ├── prompt_builder.py
│   │   ├── file_handler.py
│   │   ├── retry.py
│   │   └── pagination.py
│   │
│   ├── prompts/
│   │   ├── tutor.txt
│   │   ├── summarizer.txt
│   │   ├── coding.txt
│   │   ├── math.txt
│   │   └── system.txt
│   │
│   ├── memory/
│   │   ├── conversation.py
│   │   ├── history.py
│   │   ├── vector_store.py
│   │   └── summarizer.py
│   │
│   └── core/
│       ├── startup.py
│       ├── shutdown.py
│       ├── config_loader.py
│       └── lifespan.py
│
├── migrations/
│   └── (optional custom migration scripts)
│
├── alembic/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       ├── 001_create_users.py
│       ├── 002_create_sessions.py
│       ├── 003_create_messages.py
│       └── 004_create_feedback.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_chat.py
│   ├── test_database.py
│   ├── test_cache.py
│   ├── test_ai.py
│   ├── test_upload.py
│   ├── test_health.py
│   └── test_api.py
│
└── .github/
    └── workflows/
        ├── ci.yml
        ├── lint.yml
        └── deploy.yml

## 🏗️ **System Design Overview**

+--------------------+        +-------------------+        +------------------+
|   Frontend UI      | <--- HTTP/S ---> |   API Gateway    | <--- HTTP/S ---> |
| (React/Vue/Angle) |        +-------------------+        +------------------+
+--------------------+                |
                                        v
                               +-------------------+
                               |   Auth (JWT/OAuth)|
                               +-------------------+
                                        |
                                        v
                               +-------------------+
                               |   Rate Limiter    |
                               +-------------------+
                                        |
                                        v
                               +-------------------+
                               |   Rate Limiter    |
                               +-------------------+
                                        |
                                        v
                               +-------------------+
                               |   Request Cache   |
                               +-------------------+
                                        |
                                        v
                               +-------------------+
                               |   Request Validator |
                               +-------------------+
                                        |
                                        v
                               +-------------------+
                               |   LLM Backend     |
                               | (OpenAI / HF Infer)|
                               +-------------------+
                                        |
                                        v
                               +-------------------+
                               |   Context Store   |
                               | (Redis / PG)      |
                               +-------------------+
                                        |
                                        v
                               +-------------------+
                               |   Conversation DB |
                               | (PostgreSQL)      |
                               +-------------------+
'''
