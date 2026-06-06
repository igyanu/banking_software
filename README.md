# Secure Bank Management System

A Python-based Bank Management System that provides secure banking operations through role-based access control and email OTP verification.

## Features

### Admin Features

* Admin Login
* Create New User Accounts
* View All Users
* Delete User Accounts
* View User Details
* Manage User Information

### User Features

* Secure Login
* View Profile Details
* Deposit Money
* Withdraw Money (OTP Verification Required)
* Transfer Money to Existing Accounts (OTP Verification Required)
* Update Personal Information (OTP Verification Required)
* Recover Forgotten Password Using Email OTP
* View Account Balance
* View Transaction History

### Security Features

* Email-Based OTP Authentication
* Role-Based Access Control
* Transaction Validation
* Account Verification Before Transfers
* Secure Password Recovery
* Audit-Friendly Transaction Records
---

## Technology Stack

### Backend

* Python 3.x
* 
### Database

* SQLite (Development)

### Security

* SMTP Email Service for OTP Delivery

### Additional Libraries

* gmail
* sqlite3

---

## Implementation Structure

```text
bank-management-system/
│
├── app.py
├── database.py
├── README.md
│
├── admin/
│   ├── create_user.py
│   ├── delete_user.py
│   └── view_users.py
│
├── user/
    ├── view_profile.py
│   ├── update_profile.py
    ├── deposit.py
│   ├── withdraw.py
│   ├── transfer.py
│   └── view transaction.py
│
├── database/
│   └── bank.db
```

---

## Workflow

### User Registration

1. Admin creates a new user account.
2. User receives account credentials.
3. User logs in and manages their account.

### Money Transfer

1. User enters recipient account number.
2. System verifies account existence.
3. OTP is sent to the registered email.
4. User enters OTP.
5. Transaction is completed upon successful verification.

### Password Recovery

1. User selects "Forgot Password".
2. OTP is sent to the registered email.
3. User verifies OTP.
4. User creates a new password.

---

## Database Schema

### Users Table

| Field      | Type            |
| ---------- | --------------- |
| id         | Integer primary |
| account_no | String          |
| full_name  | String          |
| email      | String          |
| phone      | String          |
| password   | String          |
| balance    | Float           |
| created_at | Timestamp       |

### Transactions Table

| Field            | Type      |
| ---------------- | --------- |
| id               | Integer   |
| sender_account   | String    |
| receiver_account | String    |
| amount           | Float     |
| transaction_type | String    |
| transaction_date | Timestamp |

### OTP Table

| Field       | Type      |
| ----------- | --------- |
| email       | String    |
| otp_code    | String    |
---

## Installation

### Clone Repository

```bash
git clone https://github.com/igyanu/banking_software.git
```


## Future Enhancements

* Two-Factor Authentication (2FA)
* PDF Account Statements
* Real-Time Notifications
* Account Freeze/Unfreeze Feature
* REST API Integration

---

## Learning Outcomes

This project demonstrates:

* Python Development
* Authentication & Authorization
* Email Integration
* OTP Verification Systems
* Database Management
* Transaction Processing
* Backend Development Best Practices
---

## Author

Developed as a secure banking management application using Python and email-based OTP authentication.
