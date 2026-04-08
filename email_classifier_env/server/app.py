# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
FastAPI application for the Email Classifier Environment.
"""

from openenv.core.env_server.http_server import create_app

from email_classifier_env.models import EmailClassifierAction, EmailClassifierObservation
from email_classifier_env.server.email_classifier_env_environment import EmailClassifierEnvironment


app = create_app(
    EmailClassifierEnvironment,
    EmailClassifierAction,
    EmailClassifierObservation,
    env_name="email_classifier_env",
    max_concurrent_envs=1,
)