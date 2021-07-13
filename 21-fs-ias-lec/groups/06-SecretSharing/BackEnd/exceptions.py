"""Exceptions for the Secret Sharing Project."""


class SecretSharingError(Exception):
    """Signals that an error occurred in Secret Sharing."""
    def __init__(self, message: str):
        self.message = message
        super().__init__()

    def msg(self):
        return self.message


class PasswordError(SecretSharingError):
    """Signals that a password was not accepted or didn't fulfill specifications."""
    def __init__(self, message: str, password: str):
        self.message = message
        self.password = password
        super().__init__(message)

    def password(self) -> str:
        return self.password


class MappingError(SecretSharingError):
    """Signals that a Secret-to-Number mapping failed."""
    def __init__(self, message: str, mapping: tuple):
        self.message = message
        self.mapping = mapping
        super().__init__(message)

    def mapping(self) -> tuple:
        return self.mapping


class SecretPackagingError(SecretSharingError):
    def __init__(self, message: str, secret: bytes):
        self.message = message
        self._secret = secret
        super().__init__(message)

    def secret(self) -> bytes:
        return self._secret


class SubEventDecryptionError(SecretSharingError):
    def __init__(self, message: str, sub_event: dict):
        self.message = message
        self._secret = sub_event
        super().__init__(message)


class StateEncryptedError(SecretSharingError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class PackageStealError(SecretSharingError):
    def __init__(self, message: str, feed_id: bytes):
        self.message = message
        self.thief = feed_id
        super().__init__(message)

    def get_thief(self):
        return self.thief


# Exceptions


class IncomingRequestException(Exception):
    def __init__(self, message: str, name: str):
        self.name = name
        super().__init__(message)

    def get(self):
        return self.name


class RecoveryFromScratchException(Exception):
    def __init__(self, message: str, secret: bytes):
        self.secret = secret
        super().__init__(message)

    def get(self):
        return self.secret
