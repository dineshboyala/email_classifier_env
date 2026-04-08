from .client import EmailClassifierEnv
from email_classifier_env.models import Email, EmailAction, EmailObservation  # ← FIXED: old names removed

__all__ = [
    "Email",
    "EmailAction",
    "EmailObservation",
    "EmailClassifierEnv",
]