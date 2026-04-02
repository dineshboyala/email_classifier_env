# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Data models for the Email Classifier Env Environment.

The email_classifier_env environment is a simple test environment that echoes back messages.
"""
from openenv.core.env_server.types import Action, Observation
from pydantic import BaseModel, Field
from typing import List, Optional


class Email(BaseModel):
    id: int
    subject: str
    body: str
    category: Optional[str] = None


class EmailAction(Action):
    action_type: str
    email_id: int
    value: Optional[str] = None


class EmailObservation(Observation):
    goal: str
    current_email: Optional[Email]
    step: int