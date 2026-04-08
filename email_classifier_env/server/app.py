# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
FastAPI application for the Email Classifier Environment.
"""

from openenv.core.env_server.http_server import create_app

# FIXED: Use absolute imports relative to the app root in the container
# This avoids the "attempted relative import beyond top-level package" error
from models import EmailAction, EmailObservation
from server.email_classifier_env_environment import EmailClassifierEnvironment


app = create_app(
    EmailClassifierEnvironment,
    EmailAction,
    EmailObservation,
    env_name="email_classifier_env",
    max_concurrent_envs=1,
)