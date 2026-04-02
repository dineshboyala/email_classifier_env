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
import random

try:
    from ..models import Email, EmailObservation, EmailAction
except:
    from models import Email, EmailObservation, EmailAction


class EmailClassifierEnvironment(Environment):

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.emails = []
        self.task_type = "easy"

    # 🔥 RESET (with tasks)
    def reset(self) -> EmailObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)

        # 🎯 Random task selection
        self.task_type = random.choice(["easy", "medium", "hard"])

        self.emails = [
            Email(id=1, subject="Win money now", body="Click fast"),
            Email(id=2, subject="Meeting tomorrow", body="Important meeting"),
            Email(id=3, subject="Job Offer", body="We are hiring"),
        ]

        return EmailObservation(
            goal=f"Task: {self.task_type} email handling",
            current_email=self.emails[0],
            step=0
        )

    # 🔥 STEP (task-based reward system)
    def step(self, action: EmailAction):
        reward = 0.0
        done = False

        email = self.emails[self._state.step_count]

        # 🟢 EASY → basic classification
        if self.task_type == "easy":
            if "win" in email.subject.lower():
                reward = 1.0 if action.value == "spam" else 0.0
            else:
                reward = 1.0 if action.value == "important" else 0.0

        # 🟡 MEDIUM → better understanding
        elif self.task_type == "medium":
            if "meeting" in email.subject.lower():
                reward = 1.0 if action.value == "important" else 0.0
            else:
                reward = 1.0 if action.value == "spam" else 0.0

        # 🔴 HARD → decision making
        elif self.task_type == "hard":
            if action.action_type == "reply" and "meeting" in email.subject.lower():
                reward = 1.0
            elif action.action_type == "delete" and "win" in email.subject.lower():
                reward = 1.0
            else:
                reward = 0.0

        # 🔄 Move to next step
        self._state.step_count += 1

        if self._state.step_count >= len(self.emails):
            done = True
            next_email = None
        else:
            next_email = self.emails[self._state.step_count]

        return (
            EmailObservation(
                goal=f"Task: {self.task_type} email handling",
                current_email=next_email,
                step=self._state.step_count
            ),
            reward,
            done,
            {}
        )

    # ✅ REQUIRED by OpenEnv
    def state(self) -> State:
        return self._state