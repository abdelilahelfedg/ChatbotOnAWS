#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    CLU_ENDPOINT = os.environ.get("CLUEndpoint", "https://tdials.cognitiveservices.azure.com")
    CLU_KEY = os.environ.get("CLUKey", "85eV42YMvFcCfTIqhEabbNHTYRd6uAhy5MScy9Bl6IF23M6DhBg6JQQJ99ALACYeBjFXJ3w3AAAaACOGuHCY")
    CLU_PROJECT_NAME = os.environ.get("CLUProjectName", "clu-bot")
    CLU_DEPLOYMENT_NAME = os.environ.get("CLUDeploymentName", "tdia2-bot")  # Typically 'production'
    CLU_API_VERSION = "2022-10-01-preview"  # Update based on the CLU API version you're using

    
