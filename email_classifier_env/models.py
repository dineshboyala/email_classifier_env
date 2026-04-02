# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Data models for the Email Classifier Env Environment.

The email_classifier_env environment is a simple test environment that echoes back messages.
"""

from pydantic import BaseModel
from typing import List, Optional


class Email(BaseModel):
    id: int
    subject: str
    body: str
    category: Optional[str] = None  # spam / important
    priority: Optional[str] = None  # low / medium / high


class Observation(BaseModel):
    goal: str
    emails: List[Email]
    current_email: Optional[Email]
    history: List[str]
    last_action_error: bool = False


class Action(BaseModel):
    action_type: str  # classify / reply / delete / mark_important
    email_id: Optional[int] = None
    value: Optional[str] = None


class Reward(BaseModel):
    score: float
    reason: Optional[str] = None