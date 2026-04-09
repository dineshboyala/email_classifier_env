try:
    from openenv.core.env_server.http_server import create_app
except Exception as e:
    raise ImportError(
        "openenv is required. Install dependencies using: uv sync"
    ) from e


from models import EmailClassifierAction, EmailClassifierObservation
from server.email_classifier_environment import EmailClassifierEnvironment


app = create_app(
    EmailClassifierEnvironment,
    EmailClassifierAction,
    EmailClassifierObservation,
    env_name="email_classifier_env",
    max_concurrent_envs=1,
)


# OPTIONAL (for local run)
def main(host: str = "0.0.0.0", port: int = 8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()