# pylint: disable=unused-import,abstract-method,unused-argument

import random

import psynet.experiment
from flask import Markup
from psynet.asset import FastFunctionAsset
from psynet.modular_page import PushButtonControl, AudioPrompt
from psynet.page import InfoPage, SuccessfulEndPage, ModularPage
from psynet.prescreen import AntiphaseHeadphoneTest
from psynet.timeline import Timeline, Event
from psynet.trial.static import StaticTrial, StaticNode, StaticTrialMaker
from psynet.utils import get_logger

from .consent import consent
from .instructions import instructions
from .questionnaire import debrief, questionnaire
from .synth import synth_stimulus
from .volume_calibration import volume_calibration

logger = get_logger()


TRIALS_PER_PARTICIPANT = 50
N_REPEAT_TRIALS = 4

# TRIALS_PER_PARTICIPANT = 1  # For debugging
# N_REPEAT_TRIALS = 1


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


class ConsonanceTrial(StaticTrial):
    time_estimate = 7.5

    def finalize_definition(self, definition, experiment, participant):
        definition["duration"] = 10  # The original duration in Marjieh et al. was 1.3 s
        definition["lower_pitch"] = random.uniform(65, 67)
        # definition["centre_pitch"] = random.uniform(85, 85)
        definition["pitch_interval"] = random.uniform(0, 15)
        definition["upper_pitch"] = definition["lower_pitch"] + definition["pitch_interval"]
        # definition["lower_pitch"] = definition["centre_pitch"] - definition["pitch_interval"] / 2
        # definition["upper_pitch"] = definition["centre_pitch"] + definition["pitch_interval"] / 2

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


class ConsonanceTrialMaker(StaticTrialMaker):
    performance_check_type = "consistency"
    consistency_check_type = "spearman_correlation"
    give_end_feedback_passed = False

    def compute_bonus(self, score, passed):
        max_bonus = 0.40

        if score is None or score <= 0.0:
            bonus = 0.0
        else:
            bonus = max_bonus * score

        bonus = min(bonus, max_bonus)
        return bonus


class Exp(psynet.experiment.Experiment):
    label = "Carillon experiment"
    initial_recruitment_size = 1

    config = {
        "window_width": 1024,
        "window_height": 1024,
    }

    timeline = Timeline(
        consent,
        InfoPage(
            "This experiment requires you to wear headphones. Please ensure you have plugged yours in now.",
            time_estimate=5,
        ),
        volume_calibration(),
        InfoPage(
            """
            We will now perform a short listening test to verify that your audio is working properly.
            This test will be difficult to pass unless you listen carefully over your headphones.
            Press 'Next' when you are ready to start.
            """,
            time_estimate=5,
        ),
        AntiphaseHeadphoneTest(),
        instructions(),
        ConsonanceTrialMaker(
            id_="consonance_main_experiment",
            trial_class=ConsonanceTrial,
            nodes=nodes,
            expected_trials_per_participant=TRIALS_PER_PARTICIPANT,
            max_trials_per_participant=TRIALS_PER_PARTICIPANT,
            recruit_mode="n_participants",
            allow_repeated_nodes=False,
            n_repeat_trials=N_REPEAT_TRIALS,
            balance_across_nodes=False,
            target_n_participants=50,
            check_performance_at_end=True,
        ),
        questionnaire(),
        debrief(),
        SuccessfulEndPage(),
    )

