from openenv.core.env_server.http_server import create_app

try:
    from ..models import EmailAction, EmailObservation
    from .email_classifier_env_environment import EmailClassifierEnvironment
except ModuleNotFoundError:
    from models import EmailAction, EmailObservation
    from server.email_classifier_env_environment import EmailClassifierEnvironment


app = create_app(
    EmailClassifierEnvironment,
    EmailAction,
    EmailObservation,
    env_name="email_classifier_env",
    max_concurrent_envs=1,
)