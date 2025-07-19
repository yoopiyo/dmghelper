import uuid
import hashlib

SECRET_SALT = 'B3uYNLlpQYQPw1EwNY43B-xnx'

def get_device_id():
    return str(uuid.getnode())

def generate_activation_key(device_id):
    # Конкатенация ID и соли
    data = device_id + SECRET_SALT
    # Вычисление SHA-256 и получение первых 16 символов
    return hashlib.sha256(data.encode()).hexdigest()[:16]

if __name__ == "__main__":
    device_id = get_device_id()
    key = generate_activation_key(device_id)
    print(f"Device ID: {device_id}")
    print(f"Activation Key: {key}")
