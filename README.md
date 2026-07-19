# AI-Meeting-Assistants

---

# Requirements

Before running the project, make sure you have installed:

- Python 3.11+
- PostgreSQL
- A modern browser (Google Chrome recommended)

---

# Project Setup

## 1. Clone the repository

```bash
git clone <repository-url>

cd AI-Meeting-Assistants
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

## 4. Create .env File

Create a new `.env` file based on `.env.example`.

### Windows

```bash
copy .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

---

## 5. Update .env Values

Edit the `.env` file and update the values according to your local environment.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name

SECRET_KEY=your_secret_key

ACCESS_TOKEN_EXPIRE_MINUTES=30

REFRESH_TOKEN_EXPIRE_DAYS=7

MAIL_USERNAME=your_email

MAIL_PASSWORD=your_email_password
```

---

# Database Setup

## 6. Create PostgreSQL Database

Create a database in PostgreSQL:

```sql
CREATE DATABASE ai_meeting;
```

Update the database connection inside `.env`:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_meeting
```

---

## 7. Run Database Tables

Apply database migrations:

```bash
alembic upgrade head
```

---

# Run Backend

## 9. Start FastAPI Server

From the AI-Meeting-Assistants folder:

```bash
uvicorn app.main:app --reload
```

Backend will run at:

```
http://localhost:8000
```

API documentation:

```
http://localhost:8000/docs
```

---

# Frontend Setup

## 9. Enter Frontend Folder

Open another terminal:

```bash
cd frontend
```

---

## 10. Start Frontend Server

Run:

```bash
python -m http.server 5500
```

Frontend will run at:

```
http://localhost:5500
```

---

# Application Usage

## Register

Open:

```
http://localhost:5500/register.html
```

Create a new account.

---

## Login

Open:

```
http://localhost:5500/login.html
```

Login using your account.

---

