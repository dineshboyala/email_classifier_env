---
title: Email Classifier RL Environment
emoji: 📧
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 8000
base_path: /web
tags:
  - openenv
  - reinforcement-learning
  - email-classification
---

# 📧 Email Classifier RL Environment

This project implements a **Reinforcement Learning (RL) environment** for intelligent email management using the OpenEnv framework.

The objective is to simulate how an AI agent can **analyze emails, take actions, and maximize rewards** through correct decision-making.

---

# 🎯 Problem Statement

Build an environment where an AI agent:

- Classifies emails as **spam or important**
- Decides whether to **delete, reply, or classify**
- Learns to maximize reward based on correct actions

---

# 🧠 How the Environment Works

Each episode contains a sequence of emails.

At every step:
1. The agent receives an email (observation)
2. The agent selects an action
3. The environment evaluates the action
4. A reward is given
5. The next email is shown

---

# ⚙️ Action Space

The agent can perform the following actions:

| Action | Description |
|--------|------------|
| `classify` | Label the email as spam or important |
| `delete` | Remove spam emails |
| `reply` | Respond to important emails |

---

# 📊 Observation Space

Each observation contains:

- `goal` → Task description  
- `current_email` → Email details (subject, body)  
- `step` → Current step number  

---

# 🎯 Reward System

The reward system is designed to encourage correct behavior:

- ✅ Correct spam detection → Positive reward  
- ✅ Correct handling of important emails → Positive reward  
- ❌ Wrong action → Low or zero reward  

---

# 🤖 Intelligent Agent (Inference)

The project includes a **smart rule-based agent** that:

- Uses keyword-based scoring
- Identifies spam vs important emails
- Chooses optimal actions:
  - Delete spam emails
  - Reply to important emails
  - Classify when uncertain


## Project Structure

```
email_classifier_env/
├── .dockerignore         # Docker build exclusions
├── __init__.py           # Module exports
├── README.md             # Project documentation
├── openenv.yaml          # OpenEnv manifest
├── pyproject.toml        # Project metadata and dependencies
├── uv.lock               # Locked dependencies (generated)
├── client.py             # EmailClassifierEnv client
├── models.py             # Action and Observation models
├── inference.py          # Runs the intelligent agent to interact with the environment and generate actions
└── server/
    ├── __init__.py       # Server module exports
    ├── email_classifier_env_environment.py  # Core RL environment logic
    ├── app.py            # FastAPI application (HTTP + WebSocket endpoints)
    └── Dockerfile        # Container image definition

```