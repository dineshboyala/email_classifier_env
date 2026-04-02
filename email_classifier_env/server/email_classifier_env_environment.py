# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Email Classifier Env Environment Implementation.

A simple test environment that echoes back messages sent to it.
Perfect for testing HTTP server infrastructure.
"""

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State
from uuid import uuid4

# ✅ FIXED IMPORT (very important)
try:
    from ..models import Email, EmailObservation, EmailAction
except ModuleNotFoundError:
    from models import Email, EmailObservation, EmailAction


class EmailClassifierEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS = True  # ✅ good practice

    def __init__(self):
        self.state = State(episode_id=str(uuid4()), step_count=0)
        self.emails = []
        self.history = []

    def reset(self) -> EmailObservation:
        self.state = State(episode_id=str(uuid4()), step_count=0)

        self.emails = [
            Email(id=1, subject="Win a free iPhone!!!", body="Click now"),
            Email(id=2, subject="Meeting tomorrow", body="Schedule meeting at 10AM"),
            Email(id=3, subject="Job Offer", body="We are hiring you"),
        ]

        self.history = []

        return self._get_observation(error=False)

    def step(self, action: EmailAction):
        reward = 0.0
        done = False
        error = False

        try:
            # ✅ Safe check
            if self.state.step_count >= len(self.emails):
                return self._get_observation(), 0.0, True, {}

            email = self.emails[self.state.step_count]

            if action.action_type == "classify":
                if "win" in email.subject.lower():
                    reward += 0.5 if action.value == "spam" else -0.2
                else:
                    reward += 0.5 if action.value == "important" else -0.2

                email.category = action.value

            elif action.action_type == "delete":
                reward += 0.3 if email.category == "spam" else -0.2

            elif action.action_type == "reply":
                reward += 0.5 if email.category == "important" else -0.3

            else:
                reward -= 0.1

        except Exception:
            error = True
            reward -= 0.5

        self.history.append(f"{action.action_type} on email {action.email_id}")

        self.state.step_count += 1

        if self.state.step_count >= len(self.emails):
            done = True

        return self._get_observation(error), reward, done, {}

    def _get_observation(self, error=False) -> EmailObservation:
        current_email = None
        if self.state.step_count < len(self.emails):
            current_email = self.emails[self.state.step_count]

        return EmailObservation(
            goal="Classify and manage emails",
            emails=self.emails,
            current_email=current_email,
            history=self.history,
            last_action_error=error
        )