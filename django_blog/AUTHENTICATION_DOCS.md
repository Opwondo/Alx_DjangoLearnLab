# Django Blog Authentication System Documentation

## Overview
The authentication system provides user management features including registration, login, logout, and profile management. It leverages Django's built-in authentication framework while extending it with custom forms and views.

## Features

### 1. User Registration
- **URL**: `/register`
- **Template**: `register.html`
- **Form**: `UserRegisterForm` (extends Django's UserCreationForm)
- **Fields**: Username, Email, Password, Confirm Password
- **Validation**: 
  - Email uniqueness check
  - Password strength validation (Django defaults)
  - Username uniqueness (Django defaults)

### 2. User Login
- **URL**: `/login`
- **Template**: `login.html`
- **Form**: Django's AuthenticationForm
- **Process**:
  1. User submits credentials
  2. Django authenticates against database
  3. Session created upon success
  4. Redirect to profile page

### 3. User Logout
- **URL**: `/logout`
- **View**: `logout_view`
- **Process**:
  1. Django's logout() function called
  2. Session destroyed
  3. Success message displayed
  4. Redirect to home page

### 4. Profile Management
- **URL**: `/profile`
- **Template**: `profile.html`
- **Form**: `UserUpdateForm`
- **Features**:
  - View current profile info
  - Update username and email
  - View account statistics
  - Protected by login_required decorator

## Security Implementation

### CSRF Protection
- All forms include `{% csrf_token %}` template tag
- Django's CSRF middleware active

### Password Security
- Passwords hashed using Django's default PBKDF2 algorithm
- No plain text passwords stored or transmitted
- Password validation on registration

### Session Security
- Django manages sessions securely
- Session expiration on browser close
- Logout destroys session

## Testing Instructions

### Test Registration
1. Navigate to `/register`
2. Fill form with valid data:
   - Username: testuser
   - Email: test@example.com
   - Password: StrongPass123!
   - Confirm password: StrongPass123!
3. Submit form
4. Verify success message and redirect to login

### Test Login
1. Navigate to `/login`
2. Enter credentials:
   - Username: testuser
   - Password: StrongPass123!
3. Submit form
4. Verify redirect to profile page

### Test Profile Update
1. Login to access `/profile`
2. Change email address
3. Submit form
4. Verify update success message

### Test Logout
1. Click "Logout" in navigation
2. Verify success message
3. Confirm navigation changes to show Login/Register

## Error Handling

### Common Error Scenarios
1. **Duplicate Email**: Registration displays error
2. **Invalid Credentials**: Login shows error message
3. **Unauthorized Access**: Profile redirects to login
4. **Password Mismatch**: Registration form validation

## File Structure
