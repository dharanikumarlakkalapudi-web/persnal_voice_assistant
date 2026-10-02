import keyring

class CredentialVault:
    """
    Secure OS-backed credential storage.
    Uses Windows Credential Manager on Windows to store API keys and tokens securely.
    """
    SERVICE_NAME = "JarvisPlatform"

    def set_credential(self, credential_id: str, secret: str):
        """Stores a secret securely."""
        try:
            keyring.set_password(self.SERVICE_NAME, credential_id, secret)
            return True
        except Exception as e:
            print(f"[CredentialVault] Error saving credential {credential_id}: {e}")
            return False

    def get_credential(self, credential_id: str):
        """Retrieves a secret securely."""
        try:
            return keyring.get_password(self.SERVICE_NAME, credential_id)
        except Exception as e:
            print(f"[CredentialVault] Error retrieving credential {credential_id}: {e}")
            return None

    def delete_credential(self, credential_id: str):
        """Deletes a secret from the vault."""
        try:
            keyring.delete_password(self.SERVICE_NAME, credential_id)
            return True
        except Exception as e:
            # keyring throws an exception if the password doesn't exist
            return False

vault = CredentialVault()
