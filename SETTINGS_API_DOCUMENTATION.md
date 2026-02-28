# Settings API Documentation

## Overview
Backend APIs for user profile management and preferences configuration.

---

## Endpoints

### 1. Get User Profile
**Endpoint:** `GET /api/auth/profile/`

**Authentication:** Required (JWT Token)

**Description:** Retrieve the authenticated user's profile information.

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Status Codes:**
- `200 OK` - Success
- `401 Unauthorized` - Not authenticated

---

### 2. Update User Profile
**Endpoint:** `PUT /api/auth/profile/`

**Authentication:** Required (JWT Token)

**Description:** Update the authenticated user's profile information.

**Request Body:**
```json
{
  "email": "newemail@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Note:** Username cannot be changed (read-only field)

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "newemail@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Status Codes:**
- `200 OK` - Profile updated successfully
- `400 Bad Request` - Invalid data
- `401 Unauthorized` - Not authenticated

---

### 3. Get User Preferences
**Endpoint:** `GET /api/auth/preferences/`

**Authentication:** Required (JWT Token)

**Description:** Retrieve the authenticated user's preferences.

**Response:**
```json
{
  "email_notifications": false,
  "task_reminders": true,
  "daily_summary": false,
  "default_priority": "medium"
}
```

**Status Codes:**
- `200 OK` - Success
- `401 Unauthorized` - Not authenticated

**Note:** If preferences don't exist, they will be created automatically with default values.

---

### 4. Update User Preferences
**Endpoint:** `PUT /api/auth/preferences/`

**Authentication:** Required (JWT Token)

**Description:** Update the authenticated user's preferences.

**Request Body:**
```json
{
  "email_notifications": true,
  "task_reminders": true,
  "daily_summary": true,
  "default_priority": "high"
}
```

**Fields:**
- `email_notifications` (boolean) - Enable/disable email notifications
- `task_reminders` (boolean) - Enable/disable task reminders
- `daily_summary` (boolean) - Enable/disable daily summary emails
- `default_priority` (string) - Default priority for new tasks: "low", "medium", or "high"

**Response:**
```json
{
  "message": "Preferences updated successfully",
  "preferences": {
    "email_notifications": true,
    "task_reminders": true,
    "daily_summary": true,
    "default_priority": "high"
  }
}
```

**Status Codes:**
- `200 OK` - Preferences updated successfully
- `400 Bad Request` - Invalid data
- `401 Unauthorized` - Not authenticated

---

### 5. Delete Account
**Endpoint:** `DELETE /api/auth/delete-account/`

**Authentication:** Required (JWT Token)

**Description:** Permanently delete the authenticated user's account and all associated data (tasks, preferences).

**Warning:** This action is irreversible!

**Response:**
```json
{
  "message": "Account john_doe has been permanently deleted"
}
```

**Status Codes:**
- `200 OK` - Account deleted successfully
- `401 Unauthorized` - Not authenticated

**Note:** After deletion, the user will be logged out and all JWT tokens will be invalidated.

---

## Database Models

### UserPreferences Model

**Fields:**
- `user` (OneToOneField) - Link to User model
- `email_notifications` (BooleanField) - Default: False
- `task_reminders` (BooleanField) - Default: True
- `daily_summary` (BooleanField) - Default: False
- `default_priority` (CharField) - Choices: "low", "medium", "high" - Default: "medium"
- `created_at` (DateTimeField) - Auto-generated
- `updated_at` (DateTimeField) - Auto-updated

**Relationships:**
- One-to-One with User model
- Cascade delete when user is deleted

---

## Usage Examples

### Example 1: Get Profile
```bash
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Example 2: Update Profile
```bash
curl -X PUT http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Example 3: Get Preferences
```bash
curl -X GET http://127.0.0.1:8000/api/auth/preferences/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Example 4: Update Preferences
```bash
curl -X PUT http://127.0.0.1:8000/api/auth/preferences/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email_notifications": true,
    "task_reminders": true,
    "daily_summary": false,
    "default_priority": "high"
  }'
```

### Example 5: Delete Account
```bash
curl -X DELETE http://127.0.0.1:8000/api/auth/delete-account/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Frontend Integration

### JavaScript Example

```javascript
// Get auth headers
function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

// Load profile
async function loadProfile() {
    const response = await fetch('/api/auth/profile/', {
        headers: getAuthHeaders()
    });
    const data = await response.json();
    console.log(data);
}

// Update profile
async function updateProfile(profileData) {
    const response = await fetch('/api/auth/profile/', {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(profileData)
    });
    return await response.json();
}

// Load preferences
async function loadPreferences() {
    const response = await fetch('/api/auth/preferences/', {
        headers: getAuthHeaders()
    });
    const data = await response.json();
    console.log(data);
}

// Update preferences
async function updatePreferences(preferencesData) {
    const response = await fetch('/api/auth/preferences/', {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(preferencesData)
    });
    return await response.json();
}

// Delete account
async function deleteAccount() {
    const response = await fetch('/api/auth/delete-account/', {
        method: 'DELETE',
        headers: getAuthHeaders()
    });
    return await response.json();
}
```

---

## Security Considerations

1. **Authentication Required:** All endpoints require valid JWT token
2. **User Isolation:** Users can only access/modify their own data
3. **Cascade Deletion:** Deleting a user automatically deletes all related data
4. **Password Security:** Passwords are hashed and never exposed in API responses
5. **Token Invalidation:** Deleted accounts invalidate all associated tokens

---

## Error Handling

### Common Error Responses

**401 Unauthorized:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**400 Bad Request:**
```json
{
  "email": ["Enter a valid email address."],
  "default_priority": ["\"invalid\" is not a valid choice."]
}
```

**404 Not Found:**
```json
{
  "detail": "Not found."
}
```

---

## Testing

### Test Profile Update
1. Login to get access token
2. Call GET /api/auth/profile/ to see current data
3. Call PUT /api/auth/profile/ with new data
4. Verify changes in response

### Test Preferences
1. Login to get access token
2. Call GET /api/auth/preferences/ (creates default if not exists)
3. Toggle some preferences
4. Call PUT /api/auth/preferences/ with new values
5. Call GET again to verify changes

### Test Account Deletion
1. Create a test account
2. Create some tasks
3. Call DELETE /api/auth/delete-account/
4. Verify account and tasks are deleted
5. Verify login no longer works

---

## Summary

✅ **Implemented Endpoints:**
- GET /api/auth/profile/ - Get user profile
- PUT /api/auth/profile/ - Update user profile
- GET /api/auth/preferences/ - Get user preferences
- PUT /api/auth/preferences/ - Update user preferences
- DELETE /api/auth/delete-account/ - Delete account

✅ **Features:**
- Profile management (email, first name, last name)
- Notification preferences (email, reminders, daily summary)
- Default task settings (priority)
- Account deletion with cascade
- Automatic preference creation for new users
- Full frontend integration

✅ **Security:**
- JWT authentication required
- User-specific data access
- Cascade deletion
- Token invalidation on account deletion

The Settings API is now fully functional and integrated with the frontend!
