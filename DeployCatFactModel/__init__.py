import logging
from ..utils import deploy_catfact_model

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    deploy_catfact_model()
