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
        self.total_reward = 0.0

    def reset(self) -> EmailObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.total_reward = 0.0

        self.emails = [
            Email(id=1, subject="Win money now", body="Click fast"),
            Email(id=2, subject="Meeting tomorrow", body="Important meeting"),
            Email(id=3, subject="Job Offer", body="We are hiring"),
        ]

        obs = EmailObservation(
            goal="Classify emails",
            current_email=self.emails[0],
            step=0
        )
        obs.reward = 0.0
        obs.done = False

        print("RESET ONCE", flush=True)

        return obs

    def step(self, action: EmailAction) -> EmailObservation:
        idx = self._state.step_count

        # stop if finished
        if idx >= len(self.emails):
            obs = EmailObservation(
                goal="done",
                current_email=None,
                step=idx
            )
            obs.reward = 0.0
            obs.done = True
            return obs

        email = self.emails[idx]

        # reward logic
        if "win" in email.subject.lower():
            reward = 1.0 if action.value == "spam" else 0.0
        else:
            reward = 1.0 if action.value == "important" else 0.0

        self.total_reward += reward

        # move forward
        self._state.step_count += 1
        idx = self._state.step_count

        done = idx >= len(self.emails)
        next_email = None if done else self.emails[idx]

        print(f"STEP {idx} | done={done}", flush=True)

        if done:
            score = self.total_reward / len(self.emails)
            print(f"FINAL SCORE: {score:.2f}", flush=True)

        obs = EmailObservation(
            goal="Classify emails",
            current_email=next_email,
            step=idx
        )
        obs.reward = reward
        obs.done = done

        return obs

    def state(self):
        return self._state