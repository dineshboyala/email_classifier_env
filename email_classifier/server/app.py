# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
FastAPI application for the Email Classifier Environment.

This module creates an HTTP server that exposes the EmailClassifierEnvironment
over HTTP and WebSocket endpoints, compatible with EnvClient.

Endpoints:
    - POST /reset: Reset the environment
    - POST /step: Execute an action
    - GET /state: Get current environment state
    - GET /schema: Get action/observation schemas
    - WS /ws: WebSocket endpoint for persistent sessions

Usage:
    # Development (with auto-reload):
    uvicorn server.app:app --reload --host 0.0.0.0 --port 8000

    # Production:
    uvicorn server.app:app --host 0.0.0.0 --port 8000 --workers 4

    # Or run directly:
    python -m server.app
"""

try:
    from openenv.core.env_server.http_server import create_app
except Exception as e:
    raise ImportError(
        "openenv is required. Install dependencies using: uv sync"
    ) from e


# ✅ CORRECT IMPORTS (NO RELATIVE IMPORT)
from email_classifier.models import EmailClassifierAction, EmailClassifierObservation
from server.email_classifier_environment import EmailClassifierEnvironment
# ✅ CREATE APP
app = create_app(
    EmailClassifierEnvironment,
    EmailClassifierAction,
    EmailClassifierObservation,
    env_name="email_classifier_env",
    max_concurrent_envs=1,
)


# ✅ RUN SERVER
def main(host: str = "0.0.0.0", port: int = 8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()