# TaskFlow - Task Management Application

A modern, feature-rich task management web application built with Django and vanilla JavaScript.

## 🚀 Features

- **User Authentication** - Secure JWT-based registration and login
- **Task Management** - Create, edit, delete, and complete tasks
- **Priority Levels** - Organize tasks by low, medium, or high priority
- **Due Dates** - Set deadlines and track overdue tasks
- **Calendar View** - Visual monthly calendar with task display
- **Dashboard** - Overview with statistics and completion rates
- **Dark Mode** - System-wide dark theme toggle
- **Profile Management** - Upload profile pictures and customize preferences
- **Real-time Validation** - Instant feedback on form inputs
- **Responsive Design** - Works on desktop, tablet, and mobile

## 📋 Requirements

- Python 3.8+
- Django 6.0.1
- Django REST Framework 3.16.1
- djangorestframework-simplejwt 5.5.1

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd task_manager
```

2. **Install dependencies**
```bash
pip install django djangorestframework djangorestframework-simplejwt django-filter
```

3. **Run migrations**
```bash
python manage.py migrate
```

4. **Start the development server**
```bash
python manage.py runserver
```

5. **Access the application**
```
http://127.0.0.1:8000/
```

## 📱 Pages

- **Home** (`/`) - Landing page
- **Register** (`/register`) - Create new account
- **Login** (`/login`) - User authentication
- **Dashboard** (`/dashboard`) - Task overview and statistics
- **Tasks** (`/tasks`) - Full task list with filters
- **Calendar** (`/calendar`) - Monthly calendar view
- **Settings** (`/settings`) - User preferences and profile

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET/PUT /api/auth/profile/` - View/update profile
- `GET/PUT /api/auth/preferences/` - View/update preferences
- `POST /api/auth/upload-profile-image/` - Upload profile picture
- `DELETE /api/auth/delete-account/` - Delete account

### Tasks
- `GET /api/tasks/` - List all tasks (with filters)
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/<id>/` - Get task details
- `PUT/PATCH /api/tasks/<id>/` - Update task
- `DELETE /api/tasks/<id>/` - Delete task
- `GET /api/tasks/summary/` - Get task statistics
- `GET /api/tasks/calendar/` - Get calendar tasks
- `GET /api/tasks/daily-summary/` - Get daily summary

## 🎨 Key Features

### Task Completion Rate
- Track completion rates by Total, Weekly, or Monthly periods
- Visual circular progress indicator
- Navigate through past weeks/months

### Daily Summary
- Displays after 6 PM
- Shows tasks completed today, due today, due tomorrow, and overdue
- Grouped task lists with priority badges

### Validation
- Real-time form validation with instant feedback
- Password strength indicator
- Clear error messages
- Both frontend and backend validation

### Dark Mode
- Toggle in Settings
- Persists across sessions
- Applies to all pages instantly

## 📊 Database Schema

### User (Django built-in)
- Standard Django user model

### UserPreferences
- `dark_mode` - Boolean
- `default_priority` - Choice (low/medium/high)
- `profile_image` - ImageField

### Task
- `title` - CharField (max 255)
- `description` - TextField (optional)
- `status` - Choice (pending/completed)
- `priority` - Choice (low/medium/high)
- `due_date` - DateTimeField (optional)
- `user` - ForeignKey to User

## 🧪 Testing with Postman

See `POSTMAN_API_GUIDE.md` for complete API documentation and test cases.

## 📖 Documentation

- `SYSTEM_OVERVIEW.md` - Complete system architecture and features
- `PAGE_BY_PAGE_DEMO.md` - Detailed page-by-page walkthrough
- `VALIDATION_GUIDE.md` - Backend validation rules
- `FRONTEND_VALIDATION_SUMMARY.md` - Frontend validation implementation
- `POSTMAN_API_GUIDE.md` - API testing guide

## 🔒 Security

- JWT token-based authentication
- Password validation and hashing
- User data isolation
- CSRF protection
- Input validation and sanitization

## 🎯 Default Settings

- Default priority: Medium
- Dark mode: Off
- Token expiry: 60 minutes

## 📝 Usage

1. **Register** a new account
2. **Login** with your credentials
3. **Create tasks** from Dashboard or Tasks page
4. **Set priorities** and due dates
5. **Track progress** with completion rates
6. **View calendar** for monthly overview
7. **Customize** in Settings (dark mode, profile picture, default priority)

## 🐛 Troubleshooting

**Server won't start:**
- Check if port 8000 is available
- Ensure all dependencies are installed
- Run migrations: `python manage.py migrate`

**Can't login:**
- Verify credentials are correct
- Check if user account exists
- Clear browser localStorage and try again

**Profile image not showing:**
- Check media files are configured correctly
- Verify MEDIA_URL and MEDIA_ROOT in settings
- Ensure image file size is under 5MB

## 🤝 Contributing

This is a personal project. Feel free to fork and customize for your needs.

## 📄 License

This project is open source and available for personal use.

## 👨‍💻 Author

Built with Django REST Framework and vanilla JavaScript.

---

**Version:** 1.0.0  
**Last Updated:** March 2026
