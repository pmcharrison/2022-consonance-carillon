# pylint: disable=unused-import,abstract-method,unused-argument

import random

import psynet.experiment
from flask import Markup
from psynet.asset import FastFunctionAsset
from psynet.consent import NoConsent
from psynet.modular_page import PushButtonControl, AudioPrompt
from psynet.page import InfoPage, SuccessfulEndPage, ModularPage
from psynet.timeline import Timeline, Event
from psynet.trial.static import StaticTrial, StaticNode, StaticTrialMaker
from psynet.utils import get_logger

from .synth import synth_stimulus

logger = get_logger()


nodes = [
    StaticNode(
        definition={
            "timbre": timbre,
            "repetition": repetition,
        },
    )
    for timbre in ["carillon"]
    for repetition in range(50)
]


def func(path):
    pass


class ConsonanceTrial(StaticTrial):
    time_estimate = 5

    def finalize_definition(self, definition, experiment, participant):
        definition["duration"] = 10  # The original duration in Marjieh et al. was 1.3 s
        # definition["lower_pitch"] = random.uniform(79, 79)  # The current samples go from MIDI 78.56 to 92.5
        definition["centre_pitch"] = random.uniform(85, 85)
        definition["pitch_interval"] = random.uniform(0, 15)
        # definition["upper_pitch"] = definition["lower_pitch"] + definition["pitch_interval"]
        definition["lower_pitch"] = definition["centre_pitch"] - definition["pitch_interval"] / 2
        definition["upper_pitch"] = definition["centre_pitch"] + definition["pitch_interval"] / 2

        self.add_assets(
            {
                "stimulus": FastFunctionAsset(
                    function=synth_stimulus,
                    extension=".wav",
                )
            }
        )
        return definition

    def show_trial(self, experiment, participant):
        return ModularPage(
            "chord_player",
            AudioPrompt(
                self.assets["stimulus"],
                Markup("Please rate the sound for <strong>pleasantness</strong> on a scale from 1 to 7."),
            ),
            PushButtonControl(
                choices=[1, 2, 3, 4, 5, 6, 7],
                labels=[
                    "(1) Very unpleasant",
                    "(2)",
                    "(3)",
                    "(4)",
                    "(5)",
                    "(6)",
                    "(7) Very pleasant",
                ],
                arrange_vertically=True,
            ),
            events={
                "responseEnable": Event(is_triggered_by="promptEnd"),
                "submitEnable": Event(is_triggered_by="promptEnd")
            }
        )


class Exp(psynet.experiment.Experiment):
    label = "Carillon experiment"

    timeline = Timeline(
        NoConsent(),
        # To do - add Cambridge consent
        # To do - add volume calibration
        InfoPage(
            "Welcome to the experiment!",
            time_estimate=5,
        ),
        StaticTrialMaker(
            id_="consonance_main_experiment",
            trial_class=ConsonanceTrial,
            nodes=nodes,
            expected_trials_per_participant=len(nodes),
            max_trials_per_participant=len(nodes),
            recruit_mode="n_participants",
            allow_repeated_nodes=False,
            n_repeat_trials=0,
            balance_across_nodes=False,
            target_n_participants=50,
        ),
        # To do - add questionnaire
        SuccessfulEndPage(),
    )

    def __init__(self, session=None):
        super().__init__(session)
        self.initial_recruitment_size = (
            1
        )
