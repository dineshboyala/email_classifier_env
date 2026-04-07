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

        return EmailObservation(
            goal="Classify emails",
            current_email=self.emails[0],
            step=0
        )

    # 🔥 FIXED STEP FUNCTION
    def step(self, action):
        try:
            # ✅ unwrap OpenEnv action
            action = action.action

            # safety check
            if self._state.step_count >= len(self.emails):
                return (
                    EmailObservation(
                        goal="Classify emails",
                        current_email=None,
                        step=self._state.step_count
                    ),
                    0.0,
                    True,
                    {}
                )

            email = self.emails[self._state.step_count]

            # ✅ reward logic
            if "win" in email.subject.lower():
                reward = 1.0 if action.value == "spam" else 0.0
            else:
                reward = 1.0 if action.value == "important" else 0.0

            # track score
            self.total_reward += reward

            # next step
            self._state.step_count += 1

            done = self._state.step_count >= len(self.emails)

            if done:
                next_email = None
            else:
                next_email = self.emails[self._state.step_count]

            # debug logs
            print(f"[DEBUG] step={self._state.step_count}, done={done}", flush=True)

            # ✅ final score print
            if done:
                final_score = self.total_reward / len(self.emails)
                print(f"[FINAL SCORE] {final_score:.2f}", flush=True)

            return (
                EmailObservation(
                    goal="Classify emails",
                    current_email=next_email,
                    step=self._state.step_count
                ),
                reward,
                done,
                {}
            )

        except Exception as e:
            print(f"[ERROR] {str(e)}", flush=True)

            return (
                EmailObservation(
                    goal="Error occurred",
                    current_email=None,
                    step=self._state.step_count
                ),
                -1.0,
                True,
                {}
            )

    def state(self) -> State:
        return self._state