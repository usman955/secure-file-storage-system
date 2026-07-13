# main.py
import os
import sqlite3
import getpass
import io
from pathlib import Path
from database import get_db
import bcrypt
from crypto_utils import gen_salt, derive_key, encrypt_bytes, decrypt_bytes

STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

# In-memory session
SESSION = {"user": None, "enc_key": None}

def register():
    db = get_db()
    username = input("Choose username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    password = getpass.getpass("Choose password: ").encode()
    if not password:
        print("Password cannot be empty.")
        return

    salt = gen_salt()
    pw_hash = bcrypt.hashpw(password, bcrypt.gensalt())

    try:
        db.execute(
            "INSERT INTO users (username, password_hash, kdf_salt) VALUES (?, ?, ?)",
            (username, pw_hash, salt)
        )
        db.commit()
        print("Registered. You can now login.")
    except sqlite3.IntegrityError:
        print("Username already exists.")

def login():
    db = get_db()
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ").encode()

    row = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if not row:
        print("Invalid credentials.")
        return False

    if not bcrypt.checkpw(password, row["password_hash"]):
        print("Invalid credentials.")
        return False

    # derive encryption key from password + stored salt
    k = derive_key(password, row["kdf_salt"])
    SESSION["user"] = {"id": row["id"], "username": row["username"]}
    SESSION["enc_key"] = k
    print(f"Logged in as {row['username']}")
    return True

def logout():
    SESSION["user"] = None
    SESSION["enc_key"] = None
    print("Logged out.")

def upload_file():
    if not SESSION["user"]:
        print("Login required.")
        return
    path = input("Path to local file to upload: ").strip()
    if not path:
        print("No path entered.")
        return
    p = Path(path)
    if not p.exists() or not p.is_file():
        print("File not found.")
        return

    data = p.read_bytes()
    key = SESSION["enc_key"]
    nonce, ciphertext = encrypt_bytes(data, key)

    stored_name = f"{SESSION['user']['id']}_{os.urandom(6).hex()}_{p.name}.enc"
    out_path = Path(STORAGE_DIR) / stored_name
    with open(out_path, "wb") as fh:
        fh.write(nonce + ciphertext)

    db = get_db()
    db.execute(
        "INSERT INTO files (user_id, filename, stored_name, nonce, filesize) VALUES (?, ?, ?, ?, ?)",
        (SESSION["user"]["id"], p.name, stored_name, nonce, len(data))
    )
    db.commit()
    print("Upload complete. File stored encrypted.")

def list_files():
    if not SESSION["user"]:
        print("Login required.")
        return
    db = get_db()
    rows = db.execute("SELECT id, filename, filesize, uploaded_at FROM files WHERE user_id = ? ORDER BY uploaded_at DESC",
                      (SESSION["user"]["id"],)).fetchall()
    if not rows:
        print("No files uploaded.")
        return
    print(f"\nYour files ({len(rows)}):")
    print("ID | Name | Size | Uploaded")
    for r in rows:
        print(f"{r['id']} | {r['filename']} | {r['filesize']} | {r['uploaded_at']}")
    print()

def download_file():
    if not SESSION["user"]:
        print("Login required.")
        return
    file_id = input("Enter file ID to download: ").strip()
    if not file_id.isdigit():
        print("Invalid ID.")
        return
    db = get_db()
    row = db.execute("SELECT * FROM files WHERE id = ? AND user_id = ?", (int(file_id), SESSION["user"]["id"])).fetchone()
    if not row:
        print("File not found or not permitted.")
        return
    path = Path(STORAGE_DIR) / row["stored_name"]
    if not path.exists():
        print("Stored file missing.")
        return
    raw = path.read_bytes()
    nonce = raw[:12]
    ciphertext = raw[12:]
    key = SESSION["enc_key"]
    try:
        plaintext = decrypt_bytes(nonce, ciphertext, key)
    except Exception as e:
        print("Decryption failed (corrupted or wrong key).")
        return
    out_path = input("Save as (local path to save file): ").strip()
    if not out_path:
        print("No output path; operation cancelled.")
        return
    with open(out_path, "wb") as fh:
        fh.write(plaintext)
    print("File downloaded and decrypted to", out_path)

def menu():
    print("""
Secure File Storage (CLI)
1) Register
2) Login
3) Upload file (encrypt & store)
4) List my files
5) Download file (decrypt)
6) Logout
7) Exit
""")

def main_loop():
    while True:
        menu()
        choice = input("Choose: ").strip()
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            upload_file()
        elif choice == "4":
            list_files()
        elif choice == "5":
            download_file()
        elif choice == "6":
            logout()
        elif choice == "7":
            print("Bye.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    print("Simple Secure File Storage - CLI")
    main_loop()
