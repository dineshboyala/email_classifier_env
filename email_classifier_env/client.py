# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Email Classifier Environment Client."""

from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

try:
    from .models import EmailAction, EmailObservation  # ← FIXED: try/except for package vs direct run
except ImportError:
    from models import EmailAction, EmailObservation


class EmailClassifierEnv(
    EnvClient[EmailAction, EmailObservation, State]
):
    """
    Client for the Email Classifier Environment.

    Example:
        >>> with EmailClassifierEnv(base_url="http://localhost:8000") as client:
        ...     result = client.reset()
        ...     print(result.observation.current_email)
        ...
        ...     result = client.step(EmailAction(action_type="classify", email_id=1, value="spam"))
        ...     print(result.observation.current_email)

    Example with Docker:
        >>> client = EmailClassifierEnv.from_docker_image("email_classifier-env:latest")
        >>> try:
        ...     result = client.reset()
        ...     result = client.step(EmailAction(action_type="classify", email_id=1, value="spam"))
        ... finally:
        ...     client.close()
    """

    def _step_payload(self, action: EmailAction) -> Dict:
        """
        Convert EmailAction to JSON payload for step message.
        """
        return {                         # ← FIXED: matches new EmailAction fields
            "action_type": action.action_type,
            "email_id": action.email_id,
            "value": action.value,
        }

    def _parse_result(self, payload: Dict) -> StepResult[EmailObservation]:  # ← FIXED: removed @abstractmethod
        """
        Parse server response into StepResult[EmailObservation].
        """
        obs_data = payload.get("observation", {})
        observation = EmailObservation(    # ← FIXED: matches new EmailObservation fields
            goal=obs_data.get("goal", ""),
            current_email=obs_data.get("current_email"),
            step=obs_data.get("step", 0),
            done=payload.get("done", False),
            reward=payload.get("reward", 0.0),
            metadata=obs_data.get("metadata", {}),
        )

        return StepResult(
            observation=observation,
            reward=payload.get("reward", 0.0),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: Dict) -> State:
        """
        Parse server response into State object.
        """
        return State(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
        )