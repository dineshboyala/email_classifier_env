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
from typing import Optional


# ✅ Email object
class Email(BaseModel):
    id: int
    subject: str
    body: str
    category: Optional[str] = None


# ✅ Action (IMPORTANT NAME)
class EmailAction(BaseModel):
    action_type: str
    email_id: int
    value: Optional[str] = None


# ✅ Observation (IMPORTANT NAME)
class EmailObservation(BaseModel):
    goal: str
    current_email: Optional[Email]
    step: int