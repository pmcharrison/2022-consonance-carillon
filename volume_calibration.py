import os
import random

from dominate import tags

from psynet.modular_page import ModularPage, AudioPrompt
from psynet.timeline import CodeBlock, PageMaker, join, Event, Module


def volume_calibration():
    dir_ = "static/westerkerk-carillon-samples/wav"
    possible_files = os.listdir(dir_)
    return Module(
        "volume_calibration",
        CodeBlock(lambda participant: participant.var.set("volume_calibration", random.choice(possible_files))),
        PageMaker(
            lambda participant, experiment: volume_calibration_page(
                audio=os.path.join(dir_, participant.var.volume_calibration)
            ),
            time_estimate=10.0,
        )
    )


def volume_calibration_page(audio, min_time=2.5, time_estimate=5.0):
    text = tags.div()
    with text:
        tags.p(
            """
            Please listen to the following sound and adjust your
            computer's output volume until it is at a comfortable level.
            """
        )
        tags.p(
            """
            If you can't hear anything, there may be a problem with your
            playback configuration or your internet connection.
            You can refresh the page to try loading the audio again.
            """
        )

    return ModularPage(
        "volume_calibration",
        AudioPrompt(audio, text, loop=True),
        events={
            "submitEnable": Event(is_triggered_by="trialStart", delay=min_time)
        },
        time_estimate=time_estimate,
    )
