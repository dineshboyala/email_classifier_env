from .client import EmailClassifierEnv
from email_classifier_env.models import Email, EmailClassifierAction, EmailClassifierObservation  # ← FIXED: old names removed

__all__ = [
    "Email",
    "EmailClassifierAction",
    "EmailClassifierObservation",
    "EmailClassifierEnv",
]