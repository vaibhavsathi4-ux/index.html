# ChatTutor – AI‐Driven Personal Tutor (MVP)

## Overview
ChatTutor is a lightweight conversational tutor that:
1. Answers subject‑specific questions in natural language.
2. Keeps a short‑term context window for every session.
3. Stores all interactions for later analytics.

> **Author:** OpenAI Partner  
> **Last Updated:** 2024‑09‑01  

## Architecture
```
+-----------------+          +---------------+          +--------------+
|  Client (UI)     | <------> |  API Gateway  | <------> |  LLM Backend |
|  (React/Vue)    |          |  (FastAPI)    |          |  (OpenAI)    |
+-----------------+          +---------------+          +--------------+
        |                          |                          |
        |                          v                          |
        |              +-------------------------------------+
        |              |  Redis (Context cache, rate limiter)|
        |              +-------------------------------------+
        |
        |              +---------------------------+
        +------------> |  PostgreSQL (Logs & State)|
                       +---------------------------+
