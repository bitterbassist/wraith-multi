import os
import requests
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.primitives import hashes

# Load environment variables from the .env file
def load_env(file_path='.env'):
    env_vars = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                env_vars[key] = value
    return env_vars

# Encrypt the secret using the public key
def encrypt_secret(public_key, secret_value):
    public_key_bytes = b64decode(public_key)  # Decode the base64 public key

    # Load the PEM formatted public key
    public_key_obj = serialization.load_pem_public_key(public_key_bytes)

    # RSA encryption: Encrypt the secret
    encrypted = public_key_obj.encrypt(
        secret_value.encode('utf-8'),
        asymmetric_padding.OAEP(
            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Return the encrypted value as base64 encoded string
    return b64encode(encrypted).decode('utf-8')

# Function to create or update GitHub secrets using the GitHub API
def create_github_secret(repo, secret_name, secret_value, github_token, public_key):
    url = f"https://api.github.com/repos/{repo}/actions/secrets/{secret_name}"

    # Convert the secret value to Base64
    secret_value_b64 = encrypt_secret(public_key, secret_value)

    # Make the API request to create the secret
    response = requests.put(
        url,
        headers={
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github.v3+json",
        },
        json={
            "encrypted_value": secret_value_b64,
            "key_id": get_public_key(repo, github_token)[0],  # Use the key_id from get_public_key
        },
    )

    if response.status_code == 201:
        print(f"Successfully added secret: {secret_name}")
    else:
        print(f"Failed to add secret: {response.status_code} - {response.text}")

# Get the public key for encrypting the secret value
def get_public_key(repo, github_token):
    url = f"https://api.github.com/repos/{repo}/actions/secrets/public-key"
    response = requests.get(url, headers={
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json",
    })

    if response.status_code == 200:
        key_data = response.json()
        return key_data['key_id'], key_data['key']  # Return key_id and the base64 public key
    else:
        raise Exception("Failed to fetch public key")

# Main function
def main():
    repo = "bitterbassist/wraith-multi"  # Replace with your repository
    github_token = "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"  # Replace with your PAT

    # Load environment variables from the .env file
    env_vars = load_env()

    # Fetch the public key
    key_id, public_key = get_public_key(repo, github_token)

    # Create GitHub secrets
    for key, value in env_vars.items():
        create_github_secret(repo, key, value, github_token, public_key)

if __name__ == "__main__":
    main()
