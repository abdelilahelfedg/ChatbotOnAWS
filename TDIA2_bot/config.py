#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from dotenv import load_dotenv

class DefaultConfig:
    """ Bot Configuration """
    load_dotenv()

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "7d553a67-b975-47dd-8172-3cd2f6d9c8c1")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword")
    
