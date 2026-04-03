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

        # ✅ FIXED (must return object, not tuple)
        obs = EmailObservation(
            goal="Classify emails",
            current_email=self.emails[0],
            step=0
        )

        obs.reward = 0.0
        obs.done = False

        return obs

    def step(self, action: EmailAction):
        # ✅ prevent crash
        if self._state.step_count >= len(self.emails):
            obs = EmailObservation(
                goal="Classify emails",
                current_email=None,
                step=self._state.step_count
            )
            obs.reward = 0.0
            obs.done = True
            return obs

        email = self.emails[self._state.step_count]

        # ✅ simple reward logic
        if "win" in email.subject.lower():
            reward = 1.0 if action.value == "spam" else 0.0
        else:
            reward = 1.0 if action.value == "important" else 0.0

        self._state.step_count += 1

        if self._state.step_count >= len(self.emails):
            done = True
            next_email = None
        else:
            done = False
            next_email = self.emails[self._state.step_count]

        # ✅ FIXED return format (NO tuple)
        obs = EmailObservation(
            goal="Classify emails",
            current_email=next_email,
            step=self._state.step_count
        )

        obs.reward = reward
        obs.done = done

        return obs

    def state(self) -> State:
        return self._state