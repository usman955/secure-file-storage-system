# Secure File Storage System

A secure command-line file storage system developed in Python that encrypts user files before storing them locally. The project demonstrates modern cryptographic techniques including AES-256-GCM, PBKDF2-HMAC-SHA256, and bcrypt for secure authentication and file protection.

## Features

- Secure user registration and authentication
- Password hashing using bcrypt
- AES-256-GCM authenticated encryption
- PBKDF2-HMAC-SHA256 key derivation
- SQLite database for user and file metadata
- Secure encrypted file upload
- Secure file decryption during download
- Command-Line Interface (CLI)

---
## Project Overview

This project is a command-line secure file storage system that allows users to register, authenticate, upload files securely, and download them after decryption. It demonstrates the practical implementation of modern cryptographic techniques including AES-256-GCM, PBKDF2-HMAC-SHA256, and bcrypt for protecting sensitive data.
---

## Technologies Used

- Python 3
- SQLite
- Cryptography
- bcrypt

---

## Project Structure

```
secure-file-storage-system/
│
├── crypto_utils.py          # Encryption and key derivation
├── database.py              # SQLite database operations
├── init_db.py               # Database initialization
├── main.py                  # Main CLI application
├── requirements.txt
├── storage/                 # Encrypted file storage
├── LICENSE
└── README.md
```

---

## Cryptographic Workflow

### User Registration

1. User creates an account.
2. Password is hashed using bcrypt.
3. A random salt is generated for PBKDF2.
4. User credentials are securely stored in SQLite.

### User Login

1. User enters credentials.
2. Password is verified with bcrypt.
3. PBKDF2-HMAC-SHA256 derives a 256-bit encryption key.

### File Upload

1. User selects a file.
2. File is encrypted using AES-256-GCM.
3. Only encrypted data is stored.
4. File metadata is saved in SQLite.

### File Download

1. User selects a stored file.
2. Encrypted data is retrieved.
3. AES-256-GCM decrypts the file using the derived key.
4. Original file is restored.

---

## Installation

Clone the repository

```bash
git clone https://github.com/usman955/secure-file-storage-system.git
```

Move into the project directory

```bash
cd secure-file-storage-system
```

Install dependencies

```bash
pip install -r requirements.txt
```

Initialize the database

```bash
python init_db.py
```

Run the application

```bash
python main.py
```

---

## Security Features

- AES-256-GCM authenticated encryption
- PBKDF2-HMAC-SHA256 key derivation
- bcrypt password hashing
- Random salt generation
- Random nonce generation
- No plaintext password storage
- No plaintext file storage

---

## Future Improvements

- Graphical User Interface (GUI)
- Multi-factor authentication
- File sharing between users
- Cloud storage integration
- File integrity verification
- Secure key management

---

## Author

**Muhammad Usman**

GitHub: https://github.com/usman955
