# Rule Engine Application

## Overview

This application consists of a rule engine system that allows users to create, evaluate, save, and retrieve business rules. The system is implemented using a Python backend (Flask API) and a React frontend. The backend exposes RESTful APIs for interacting with the rule engine, and the frontend provides a user-friendly interface for interacting with the rules.

---

## Components

### 1. **Backend (Python - Flask)**

The backend is built using **Flask** and provides an API for managing rules. The backend also uses **SQLite** to store the rules in the database.

- **API Endpoints:**
  - `POST /api/rules`: Create a new rule.
  - `GET /api/rules`: Retrieve all saved rules.
  - `GET /api/rules/:id`: Retrieve a specific rule by ID.
  - `POST /api/rules/evaluate`: Evaluate a rule based on the provided data.

- **Technologies:**
  - Python
  - Flask
  - SQLite
  - JSON Web Tokens (JWT) for security (if added later)
  - CORS (Cross-Origin Resource Sharing) for frontend-backend interaction

- **Database:**
  - SQLite database (`rule_engine.db`)
  - `rules` table stores rule data (ID, rule string, and AST).
  
---

### 2. **Frontend (React)**

The frontend is built using **React** and **Material UI**. It provides a UI to:
  - Create a rule.
  - View existing rules.
  - Evaluate rules.
  - Save rules in the backend database.

- **Technologies:**
  - React
  - Material UI (for styling)
  - Axios (for API requests)

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python** 3.x
- **Node.js** and **npm** (for React)
- **SQLite** (for the backend database)
- **Axios** (installed in the frontend React app for making API requests)

---

## Installation

### Step 1: Setting up the Backend (Python)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/akashku01/rule-engine.git
   cd rule-engine
