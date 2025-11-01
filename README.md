

A **Django REST API** application for managing tasks and notes with file upload support, fully containerized using **Docker** and powered by **PostgreSQL**.

---

## 🔍 Overview
This project provides a complete backend system with:
- **User Authentication** (Signup, Login, Logout using Tokens)
- **Task Management** (CRUD operations + mark complete/incomplete)
- **Notes Management** (CRUD + file uploads linked to tasks)
- **Swagger / ReDoc API Docs**
- **PostgreSQL Database** managed via Docker and pgAdmin

---

## 🧰 Tech Stack
- **Backend:** Django 4.2, Django REST Framework 3.14  
- **Database:** PostgreSQL 15  
- **Containerization:** Docker & Docker Compose  
- **Documentation:** drf-yasg (Swagger & ReDoc)

---

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites
- Docker Desktop installed  
- PowerShell / Terminal available

### 2️⃣ Run the Application
```bash
# Build and start all containers
docker compose up --build
Once running:

Service	URL	Description
API Base	http://localhost:8000	Main backend 

pgAdmin Credentials:

pgsql
Copy code
Email: admin@admin.com
Password: admin123
Database Connection:

yaml
Copy code
Host: db
Port: 5432
Database: tasknotesdb
Username: dbuser
Password: dbpass123
🔑 API Endpoints
🧍 Authentication Endpoints
Method	Endpoint	Description
POST	/api/auth/signup/	Register a new user
POST	/api/auth/login/	Login and receive auth token
POST	/api/auth/logout/	Logout current user
GET	/api/auth/profile/	Retrieve authenticated user profile

✅ Task Endpoints
Method	Endpoint	Description
GET	/api/tasks/	List all user tasks
POST	/api/tasks/	Create a new task
GET	/api/tasks/{id}/	Retrieve specific task details
PUT	/api/tasks/{id}/	Update an existing task
DELETE	/api/tasks/{id}/	Delete a task
POST	/api/tasks/{id}/mark_complete/	Mark task as completed
POST	/api/tasks/{id}/mark_incomplete/	Mark task as pending
GET	/api/tasks/completed/	List all completed tasks
GET	/api/tasks/pending/	List all pending tasks

🗒️ Note Endpoints
Method	Endpoint	Description
GET	/api/notes/	List all user notes
POST	/api/notes/	Create a new note (supports file upload)
GET	/api/notes/{id}/	Retrieve a specific note
PUT	/api/notes/{id}/	Update a note
DELETE	/api/notes/{id}/	Delete a note
GET	/api/notes/?task={task_id}	List all notes linked to a task
GET	/api/notes/by_task/?task_id={id}	Filter notes by task

🧪 Common Commands
bash
Copy code
# Run database migrations
docker compose exec web python manage.py migrate

# Create Django superuser
docker compose exec web python manage.py createsuperuser

# Run all tests
docker compose exec web python manage.py test
🛡️ Deployment Notes
Change SECRET_KEY and set DEBUG=False in production.

Uploaded files are stored in /app/media/notes/{user_id}/.

To rebuild the stack cleanly:

bash
Copy code
docker compose down -v && docker compose up --build