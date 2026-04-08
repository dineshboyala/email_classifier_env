from .client import EmailClassifierEnv
from .models import Email, EmailAction, EmailObservation  # ← FIXED: old names removed

__all__ = [
    "Email",
    "EmailAction",
    "EmailObservation",
    "EmailClassifierEnv",
]