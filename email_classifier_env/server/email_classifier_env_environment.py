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

try:
    from ..models import Email, EmailObservation, EmailAction
except:
    from models import Email, EmailObservation, EmailAction


class EmailClassifierEnvironment(Environment):

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.emails = []

    def reset(self) -> EmailObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)

        self.emails = [
            Email(id=1, subject="Win money now", body="Click fast"),
            Email(id=2, subject="Meeting tomorrow", body="Important meeting"),
            Email(id=3, subject="Job Offer", body="We are hiring"),
        ]

        return EmailObservation(
            goal="Classify emails correctly",
            current_email=self.emails[0],
            step=0
        )

    def step(self, action: EmailAction):
        reward = 0.0
        done = False

        email = self.emails[self._state.step_count]

        if "win" in email.subject.lower():
            reward = 1.0 if action.value == "spam" else -1.0
        else:
            reward = 1.0 if action.value == "important" else -1.0

        self._state.step_count += 1

        if self._state.step_count >= len(self.emails):
            done = True
            next_email = None
        else:
            next_email = self.emails[self._state.step_count]

        return (
            EmailObservation(
                goal="Classify emails correctly",
                current_email=next_email,
                step=self._state.step_count
            ),
            reward,
            done,
            {}
        )

    # ✅ THIS WAS MISSING (VERY IMPORTANT)
    def state(self) -> State:
        return self._state