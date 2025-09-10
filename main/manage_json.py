from cryptography.fernet import Fernet
import json
import os
from manage_database import User
from main import db

# You should store this key securely!
FERNET_KEY = os.environ.get("FERNET_KEY") or Fernet.generate_key()
fernet = Fernet(FERNET_KEY)

def generate_data_json(user_id):
    user = User.query.get_or_404(user_id)
    data = {}  # Empty, as no data is specified
    json_filename = f"user_{user_id}_data.json"
    json_filepath = os.path.join("data", json_filename)
    # Encrypt the empty data
    encrypted_data = fernet.encrypt(json.dumps(data).encode())
    with open(json_filepath, 'wb') as json_file:
        json_file.write(encrypted_data)
    user.jsonfl = json_filepath
    db.session.commit()

def delete_data_json(user_id):
    user = User.query.get_or_404(user_id)
    if user.jsonfl and os.path.exists(user.jsonfl):
        os.remove(user.jsonfl)
        user.jsonfl = ""
        db.session.commit()

def get_data_json(user_id):
    user = User.query.get_or_404(user_id)
    if user.jsonfl and os.path.exists(user.jsonfl):
        with open(user.jsonfl, 'rb') as json_file:
            encrypted_data = json_file.read()
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
            data = json.loads(decrypted_data.decode())
            return data
        except Exception:
            return None
    return None

def add_new_entry(user_id, entry, content):
    user = User.query.get_or_404(user_id)
    if user.jsonfl and os.path.exists(user.jsonfl):
        with open(user.jsonfl, 'rb') as json_file:
            encrypted_data = json_file.read()
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
            data = json.loads(decrypted_data.decode())
        except Exception:
            data = {}
        data[entry] = content
        encrypted_data = fernet.encrypt(json.dumps(data).encode())
        with open(user.jsonfl, 'wb') as json_file:
            json_file.write(encrypted_data)
        return True
    return False