# Task Manager - Complete Implementation

## ✅ Fully Implemented Features

### 🔐 Authentication System

**Backend API Endpoints:**
- `POST /api/auth/register/` - User registration
  - Fields: username, email, password, password2, first_name, last_name
  - Returns: JWT tokens + user data
  
- `POST /api/auth/login/` - User login
  - Fields: username, password
  - Returns: JWT access & refresh tokens
  
- `POST /api/auth/token/refresh/` - Refresh expired tokens

**Frontend Pages:**
- `/` - Home page with login/register buttons
- `/register` - User registration form
- `/login` - User login form

### 📋 Task Management System

**Backend API Endpoints:**
- `GET /api/tasks/` - List all user's tasks
  - Query params: `?status=pending/completed` `?priority=low/medium/high`
  
- `POST /api/tasks/` - Create new task
  - Fields: title, description, priority, due_date
  
- `GET /api/tasks/{id}/` - Get single task details

- `PUT /api/tasks/{id}/` - Update existing task

- `PATCH /api/tasks/{id}/` - Partial update (e.g., mark as completed)

- `DELETE /api/tasks/{id}/` - Delete task

- `GET /api/tasks/summary/` - Get task statistics
  - Returns: total_tasks, completed_tasks, pending_tasks, overdue_tasks

**Frontend Page:**
- `/tasks` - Full task management dashboard
  - View all tasks
  - Create new tasks
  - Edit existing tasks
  - Delete tasks
  - Mark tasks as completed
  - Filter by status and priority
  - View task statistics
  - Responsive design

## 🗄️ Database Models

### User Model
- Django's built-in User model
- Fields: username, email, password, first_name, last_name

### Task Model
- user (ForeignKey to User)
- title (CharField)
- description (TextField, optional)
- status (CharField: pending/completed)
- priority (CharField: low/medium/high)
- due_date (DateTimeField, optional)
- created_at (DateTimeField, auto)
- updated_at (DateTimeField, auto)

## 🔒 Security Features

- JWT token-based authentication
- Password validation (Django validators)
- User-specific task access (users only see their own tasks)
- CSRF protection
- Secure password hashing
- Authorization checks on all task endpoints

## 🚀 How to Use

### 1. Start the Server
```bash
python manage.py runserver
```

### 2. Access the Application
Open browser: `http://127.0.0.1:8000/`

### 3. Complete User Flow

**Step 1: Register**
1. Click "Register" on home page
2. Fill in registration form
3. Submit → Automatically redirected to tasks page

**Step 2: Login (for returning users)**
1. Click "Login" on home page
2. Enter username and password
3. Submit → Redirected to tasks page

**Step 3: Manage Tasks**
1. View task summary (total, completed, pending, overdue)
2. Click "+ New Task" to create a task
3. Fill in task details (title, description, priority, due date)
4. View all your tasks in the list
5. Filter tasks by status or priority
6. Mark tasks as completed with ✓ button
7. Edit tasks with "Edit" button
8. Delete tasks with "Delete" button
9. Logout when done

## 📁 Project Structure

```
task_manager/
├── accounts/                    # Authentication app
│   ├── serializers.py          # RegisterSerializer, UserSerializer
│   ├── views.py                # RegisterView
│   └── urls.py                 # /api/auth/* endpoints
│
├── tasks/                       # Task management app
│   ├── models.py               # Task model
│   ├── serializers.py          # TaskSerializer
│   ├── views.py                # TaskListCreateView, TaskDetailView, TaskSummaryView
│   ├── urls.py                 # /api/tasks/* endpoints
│   └── permissions.py          # IsOwner permission
│
├── templates/
│   ├── home.html               # Landing page
│   ├── register.html           # Registration form
│   ├── login.html              # Login form
│   └── tasks.html              # Task management dashboard
│
├── task_manager/
│   ├── settings.py             # JWT & REST framework config
│   ├── urls.py                 # Main URL routing
│   └── views.py                # Page view functions
│
└── db.sqlite3                  # SQLite database
```

## 🧪 API Testing Examples

### Register a User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
  }'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "password": "SecurePass123!"
  }'
```

### Create a Task (requires token)
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Complete project",
    "description": "Finish the task manager",
    "priority": "high",
    "due_date": "2026-03-01T10:00:00Z"
  }'
```

### Get All Tasks
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Task Summary
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/summary/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📊 Features Summary

| Feature | Backend API | Frontend UI | Status |
|---------|-------------|-------------|--------|
| User Registration | ✅ | ✅ | Complete |
| User Login | ✅ | ✅ | Complete |
| Token Refresh | ✅ | ✅ | Complete |
| Create Task | ✅ | ✅ | Complete |
| List Tasks | ✅ | ✅ | Complete |
| View Task | ✅ | ✅ | Complete |
| Update Task | ✅ | ✅ | Complete |
| Delete Task | ✅ | ✅ | Complete |
| Filter Tasks | ✅ | ✅ | Complete |
| Task Summary | ✅ | ✅ | Complete |
| Mark Complete | ✅ | ✅ | Complete |

## 🎯 Status: 100% Complete

All planned features are fully implemented with both backend APIs and frontend interfaces!

## 🔄 User Flow Diagram

```
Home Page (/)
    ↓
    ├─→ Register (/register)
    │       ↓
    │   [Create Account]
    │       ↓
    └─→ Login (/login)
            ↓
        [Authenticate]
            ↓
    Tasks Dashboard (/tasks)
        ↓
        ├─→ View Tasks
        ├─→ Create Task
        ├─→ Edit Task
        ├─→ Delete Task
        ├─→ Mark Complete
        ├─→ Filter Tasks
        └─→ View Summary
```

## 🎨 UI Features

- Modern gradient design
- Responsive layout
- Interactive task cards
- Modal forms for create/edit
- Color-coded priority badges
- Status indicators
- Real-time filtering
- Smooth animations
- User-friendly error messages

## 🚀 Ready to Use!

Your Task Manager is fully functional and ready for production use!
